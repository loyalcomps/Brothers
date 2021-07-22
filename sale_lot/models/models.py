# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    lot_id = fields.Many2one('stock.production.lot', string="Lot/Serial Number", ondelete='restrict',
                             domain="[('product_id', '=', product_id), '|', ('company_id', '=', False), "
                                    "('company_id', '=', company_id)]", check_company=True)
    mrp = fields.Float(string='MRP', digits='Product Price', related='lot_id.mrp', store=True)

    @api.onchange('lot_id')
    def lot_id_change(self):
        if not self.lot_id:
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position'),
                lot_id=self.lot_id.id
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product),
                                                                                      product.taxes_id, self.tax_id,
                                                                                      self.company_id)


class ProductProduct(models.Model):
    _inherit = "product.product"

    # @api.depends_context('lot_id')
    # def _compute_product_price(self):
    #     super(ProductProduct, self)._compute_product_price()

    def price_compute(self, price_type, uom=False, currency=False, company=None):
        # lot wise price compute
        if self._context.get('lot_id'):
            lot_id = self.env['stock.production.lot'].browse(self._context['lot_id'])
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
                prices[product.id] = lot_id.mrp or 0.0
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

