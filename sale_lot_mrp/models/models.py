# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class StockMoveline(models.Model):
    _inherit = "stock.move.line"

    def name_get(self):
        result = super(StockMoveline, self).name_get()
        if self.env.context.get('show_mrp'):
            result = []
            for stock in self:
                name = str(stock.mrp)
                result.append((stock.id, name))
        return result


    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     result = super(StockMoveline, self)._name_search(name, args, operator, limit, name_get_uid)
    #     args = args or []
    #     domain = []
    #     if self._context.get('show_mrp'):
    #         domain = ['|', ('mrp', operator, name), ('product_id', operator, name)]
    #     stock_move_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
    #     return self.browse(stock_move_ids).name_get()

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    mrp_value = fields.Many2one('stock.move.line',string='MRP',store=True)
    qty_available = fields.Float(string='On Hand',store=True)

    @api.onchange('product_id')
    def _get_lot_mrps(self):
        mrp_float =[]
        for product in self:
            product.qty_available=product.product_id.qty_available
            lot_mrp = product.product_id.mrp_ids
            if lot_mrp:
                for rec in lot_mrp:
                    mrp_float.append(rec.id)

        res = {}
        res['domain'] = {'mrp_value': [('id', 'in', mrp_float)]}
        return res

    @api.onchange('mrp_value')
    def mrp_value_change(self):
        if not self.mrp_value:
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            self.mrp_value.name_get()
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position'),
                mrp_value=self.mrp_value.id
            )
            # self.order_id.pricelist_id.item_ids._compute_price(self.mrp_value.mrp,self.product_uom, product)
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product),
                                                                                      product.taxes_id, self.tax_id,
                                                                                      self.company_id)


class ProductProduct(models.Model):
    _inherit = "product.product"

    def price_compute(self, price_type, uom=False, currency=False, company=None):
        # mrp wise price compute
        if self._context.get('mrp_value'):
            move_line_id = self.env['stock.move.line'].browse(self._context['mrp_value'])
            # mrp_value = self._context.get('mrp_value')
            if not uom and self._context.get('uom'):
                uom = self.env['uom.uom'].browse(self._context['uom'])
            if not currency and self._context.get('currency'):
                currency = self.env['res.currency'].browse(self._context['currency'])

            products = self
            if price_type == 'standard_price':
                # standard_price field can only be seen by users in base.group_user
                # Thus, in order to compute the sale price from the cost for users not in this group
                # We fetch the standard price as the superuser
                products = self.with_company(company or self.env.company).sudo()

            prices = dict.fromkeys(self.ids, 0.0)
            for product in products:
                prices[product.id] = move_line_id.mrp or 0.0
                if price_type == 'list_price':
                    prices[product.id] += product.price_extra
                    # we need to add the price from the attributes that do not generate variants
                    # (see field product.attribute create_variant)
                    if self._context.get('no_variant_attributes_price_extra'):
                        # we have a list of price_extra that comes from the attribute values, we need to sum all that
                        prices[product.id] += sum(self._context.get('no_variant_attributes_price_extra'))

                if uom:
                    prices[product.id] = product.uom_id._compute_price(prices[product.id], uom)

                # Convert from current user company currency to asked one
                # This is right cause a field cannot be in more than one currency
                if currency:
                    prices[product.id] = product.currency_id._convert(
                        prices[product.id], currency, product.company_id, fields.Date.today())

            return prices
        else:
            return super(ProductProduct, self).price_compute(price_type, uom=uom, currency=currency, company=company)

