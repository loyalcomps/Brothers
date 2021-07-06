# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    mrp_margin = fields.Float(string='MRP Margin', default=0, digits="Product Price")
    is_tax_margin = fields.Boolean(string='Is Include Tax Margin', default=False)

    def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
        price = super(PricelistItem, self)._compute_price(price, price_uom, product, quantity=quantity, partner=partner)
        self.ensure_one()
        if self.mrp_margin:
            mrp_margin = (100 + (100 * (self.mrp_margin / 100))) / 100
            price = price / mrp_margin
        if self.is_tax_margin:
            if product.taxes_id:
                tax_per = product.taxes_id[0].amount
                tax_margin = (100 + (100 * (tax_per / 100))) / 100
                price = price / tax_margin
        return price


    # def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
    #     """Compute the unit price of a product in the context of a pricelist application.
    #        The unused parameters are there to make the full context available for overrides.
    #     """
    #     self.ensure_one()
    #     convert_to_price_uom = (lambda price: product.uom_id._compute_price(price, price_uom))
    #     if self.compute_price == 'fixed':
    #         price = convert_to_price_uom(self.fixed_price)
    #     elif self.compute_price == 'percentage':
    #         price = (price - (price * (self.percent_price / 100))) or 0.0
    #     else:
    #         # complete formula
    #         if self.mrp_margin or self.is_tax_margin:
    #             if self.mrp_margin:
    #                 mrp_margin = (100 + (100 * (self.mrp_margin / 100))) / 100
    #                 price = price / mrp_margin
    #             if self.is_tax_margin:
    #                 if product.taxes_id:
    #                     tax_per = product.taxes_id[0].amount
    #                     tax_margin = (100 + (100 * (tax_per / 100))) / 100
    #                     price = price / tax_margin
    #         else:
    #             price_limit = price
    #             price = (price - (price * (self.price_discount / 100))) or 0.0
    #             if self.price_round:
    #                 price = tools.float_round(price, precision_rounding=self.price_round)
    #
    #             if self.price_surcharge:
    #                 price_surcharge = convert_to_price_uom(self.price_surcharge)
    #                 price += price_surcharge
    #
    #             if self.price_min_margin:
    #                 price_min_margin = convert_to_price_uom(self.price_min_margin)
    #                 price = max(price, price_limit + price_min_margin)
    #
    #             if self.price_max_margin:
    #                 price_max_margin = convert_to_price_uom(self.price_max_margin)
    #                 price = min(price, price_limit + price_max_margin)
    #     return price