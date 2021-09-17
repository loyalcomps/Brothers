# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends('move_line_ids_without_package.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            partner_id = order.partner_id if order.partner_id else order.company_id.partner_id
            for line in order.move_line_ids_without_package:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    taxes = line.taxes_id.compute_all(line.price_unit, line.picking_id.currency_id, line.qty_done,
                                                      product=line.product_id, partner=partner_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position',
        domain="[('company_id', '=', company_id)]", check_company=True,
        help="Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices."
             "The default value comes from the customer.")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_set_fiscal(self):
        """
        Trigger the change of fiscal position when the shipping address is modified.
        """
        if not self.partner_id:
            self.update({
                'fiscal_position_id': False,
            })
            return
        self.fiscal_position_id = self.env['account.fiscal.position'].with_context(
            force_company=self.company_id.id).get_fiscal_position(
            self.partner_id.id, False)
        return {}

    @api.onchange('fiscal_position_id')
    def _compute_tax_id(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed on the SO.
        """
        for order in self:
            order.move_line_ids_without_package._compute_tax_id()

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        res = super(StockMove, self)._prepare_move_line_vals(quantity, reserved_quant)
        if res and 'product_id' in res:
            product_id = self.env['product.product'].browse(res['product_id'])
            fpos = self.picking_id.fiscal_position_id or self.picking_id.partner_id.property_account_position_id

            for product in product_id:
                price_unit = product.lst_price if self.picking_id.picking_type_code in ['internal',
                                                                                 'outgoing'] else product.standard_price

                taxes_id = product.taxes_id if self.picking_id.picking_type_code in ['internal','outgoing'] else \
                    product.supplier_taxes_id
            taxes = taxes_id.filtered(lambda r: r.company_id == self.picking_id.company_id)
            product_tax_id = fpos.map_tax(taxes, product_id, self.picking_id.partner_id) if fpos else taxes
            res.update({'price_unit': price_unit, 'taxes_id': product_tax_id, })

        return res


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _compute_tax_id(self):
        for line in self:
            fpos = line.picking_id.fiscal_position_id or line.picking_id.partner_id.property_account_position_id
            # If company_id is set in the picking, always filter taxes by the company
            if line.picking_id.picking_type_code in ['internal','outgoing']:
                taxes_id = line.product_id.taxes_id
            else:
                taxes_id = line.product_id.supplier_taxes_id
            taxes = taxes_id.filtered(lambda r: r.company_id == line.picking_id.company_id)
            line.taxes_id = fpos.map_tax(taxes, line.product_id, line.picking_id.partner_id) if fpos else taxes

    @api.depends('qty_done', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            partner_id = line.picking_id.partner_id if line.picking_id.partner_id else line.picking_id.company_id.partner_id
            taxes = line.taxes_id.compute_all(line.price_unit, line.picking_id.currency_id, line.qty_done,
                                              product=line.product_id, partner=partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    price_unit = fields.Float(string='Unit Price',  digits='Product Price')
    taxes_id = fields.Many2many('account.tax', string='Taxes',
                                domain=['|', ('active', '=', False), ('active', '=', True)])
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Monetary(compute='_compute_amount', string='Tax', store=True)

    @api.onchange('product_id', 'product_uom_id')
    def onchange_product_id(self):
        if self.product_id:
            price_unit = self.product_id.lst_price if self.picking_id.picking_type_code in ['internal',
                                                                         'outgoing'] else self.product_id.standard_price

            # taxes_id = [(6, 0, self.product_id.taxes_id.ids)] if self.picking_id.picking_type_code in ['internal',
            #                                                                         'outgoing'] else [
            #     (6, 0, self.product_id.supplier_taxes_id.ids)]
            # self.update({'price_unit': price_unit, 'taxes_id': taxes_id, })
            self._compute_tax_id()
            self.update({'price_unit': price_unit})



