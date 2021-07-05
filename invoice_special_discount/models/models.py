# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    special_discount = fields.Float(string='Special Discount', digits='Discount', default=0.0)

    @api.onchange('special_discount')
    def _onchange_special_discount(self):
        if self.invoice_line_ids and self.special_discount:
            for line in self.invoice_line_ids:
                line.discount = self.special_discount
                line._onchange_price_subtotal()
                line.recompute_tax_line = True
                self._onchange_invoice_line_ids()



