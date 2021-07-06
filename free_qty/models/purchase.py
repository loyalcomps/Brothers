# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    free_qty = fields.Float(string='Free Qty', digits='Product Unit of Measure', default=0.0)
    free_qty_invoiced = fields.Float(compute='_compute_qty_invoiced', string="Billed Free Qty", digits='Product Unit of Measure',
                                store=True)
    free_qty_to_invoice = fields.Float(compute='_compute_qty_invoiced', string='To Invoice Free Qty', store=True,
                                  readonly=True,
                                  digits='Product Unit of Measure')

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        res = super(PurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        self.ensure_one()
        free_qty, product_uom = self.product_uom._adjust_uom_quantities(self.free_qty, self.product_id.uom_id)
        res['product_uom_qty'] += free_qty
        return res

    @api.depends('free_qty', 'invoice_lines.free_qty')
    def _compute_qty_invoiced(self):
        super(PurchaseOrderLine, self)._compute_qty_invoiced()
        for line in self:
            qty = 0.0
            for inv_line in line.invoice_lines:
                if inv_line.move_id.state not in ['cancel']:
                    if inv_line.move_id.move_type == 'in_invoice':
                        qty += inv_line.product_uom_id._compute_quantity(inv_line.free_qty, line.product_uom)
                    elif inv_line.move_id.move_type == 'in_refund':
                        qty -= inv_line.product_uom_id._compute_quantity(inv_line.free_qty, line.product_uom)
            line.free_qty_invoiced = qty
            if line.order_id.state in ['purchase', 'done']:
                line.free_qty_to_invoice = line.free_qty - line.free_qty_invoiced
                if line.product_id.purchase_method != 'purchase':
                    line.qty_to_invoice = line.qty_received - line.qty_invoiced - line.free_qty
            else:
                line.free_qty_to_invoice = 0

    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        self.ensure_one()
        res.update({
            'free_qty': self.free_qty_to_invoice
            })
        return res
