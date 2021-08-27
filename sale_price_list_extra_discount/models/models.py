# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import get_lang


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    extra_discount = fields.Float(string='Extra Discount(%)', default=0.0, digits="Product Price")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_prices(self):
        self.ensure_one()
        lines_to_update = []
        for line in self.order_line.filtered(lambda line: not line.display_type):
            product = line.product_id.with_context(
                partner=self.partner_id,
                quantity=line.product_uom_qty,
                date=self.date_order,
                pricelist=self.pricelist_id.id,
                uom=line.product_uom.id,
                mrp_value=line.mrp_value.id
            )
            product_context = dict(self.env.context, partner_id=self.partner_id.id,
                                   date=self.date_order, uom=line.product_uom.id,mrp_value = line.mrp_value.id)
            final_price, rule_id = self.pricelist_id.with_context(product_context).get_product_price_rule(
                product or line.product_id, line.product_uom_qty or 1.0, self.partner_id)
            if rule_id and self.pricelist_id.discount_policy == 'with_discount':
                extra_discount = self.env['product.pricelist.item'].browse(rule_id).extra_discount
            else:
                extra_discount = 0
            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                line._get_display_price(product), line.product_id.taxes_id, line.tax_id, line.company_id)
            if self.pricelist_id.discount_policy == 'without_discount':
                discount = max(0, (price_unit - product.price) * 100 / price_unit)
            else:
                discount = extra_discount
            lines_to_update.append((1, line.id, {'price_unit': price_unit, 'discount': discount}))
        self.update({'order_line': lines_to_update})
        self.show_update_pricelist = False
        self.message_post(body=_("Product prices have been recomputed according to pricelist <b>%s<b> ",
                                 self.pricelist_id.display_name))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if not self.product_id:
            return
        vals = {}
        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order,
                               uom=self.product_uom.id)
        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id,
            mrp_value=self.mrp_value.id,
            fiscal_position = self.env.context.get('fiscal_position'),
        )

        final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(
            product or self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        if rule_id and self.order_id.pricelist_id.discount_policy == 'with_discount':
            vals['discount'] = self.env['product.pricelist.item'].browse(rule_id).extra_discount
        else:
            vals['discount'] = 0
        self.update(vals)
        return res


