# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    free_qty = fields.Float(string='Free Qty', digits='Product Unit of Measure', default=0.0)
    free_qty_to_invoice = fields.Float(
        compute='_get_to_invoice_free_qty', string='To Invoice Free Qty', store=True, readonly=True,
        digits='Product Unit of Measure')
    free_qty_invoiced = fields.Float(
        compute='_get_invoice_free_qty', string='Invoiced Free Qty', store=True, readonly=True,
        compute_sudo=True,
        digits='Product Unit of Measure')

    @api.depends('free_qty_invoiced', 'free_qty', 'order_id.state')
    def _get_to_invoice_free_qty(self):
        """
        Compute the free quantity to invoice.
        """
        for line in self:
            if line.order_id.state in ['sale', 'done']:
                line.free_qty_to_invoice = line.free_qty - line.free_qty_invoiced
            else:
                line.free_qty_to_invoice = 0

    @api.depends('invoice_lines.move_id.state', 'invoice_lines.free_qty', 'untaxed_amount_to_invoice')
    def _get_invoice_free_qty(self):
        """
            Compute the free quantity invoiced. If case of a refund, the free quantity invoiced is decreased.
        """
        for line in self:
            free_qty_invoiced = 0.0
            for invoice_line in line.invoice_lines:
                if invoice_line.move_id.state != 'cancel':
                    if invoice_line.move_id.move_type == 'out_invoice':
                        free_qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.free_qty,
                                                                                      line.product_uom)
                    elif invoice_line.move_id.move_type == 'out_refund':
                        if not line.is_downpayment or line.untaxed_amount_to_invoice == 0:
                            free_qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.free_qty,
                                                                                          line.product_uom)
            line.free_qty_invoiced = free_qty_invoiced

    @api.depends('free_qty')
    def _get_to_invoice_qty(self):
        super(SaleOrderLine, self)._get_to_invoice_qty()
        for line in self:
            if line.order_id.state in ['sale', 'done']:
                if line.product_id.invoice_policy != 'order':
                    line.qty_to_invoice = line.qty_delivered - line.qty_invoiced - line.free_qty
                    
    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Launch procurement group run method with required/custom fields genrated by a
        sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
        depending on the sale order line product rule.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        procurements = []
        for line in self:
            line = line.with_company(line.company_id)
            if line.state != 'sale' or not line.product_id.type in ('consu', 'product'):
                continue
            qty = line._get_qty_procurement(previous_product_uom_qty)
            if float_compare(qty, line.product_uom_qty + line.free_qty, precision_digits=precision) >= 0:
                continue

            group_id = line._get_procurement_group()
            if not group_id:
                group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                line.order_id.procurement_group_id = group_id
            else:
                # In case the procurement group is already created and the order was
                # cancelled, we need to update certain values of the group.
                updated_vals = {}
                if group_id.partner_id != line.order_id.partner_shipping_id:
                    updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
                if group_id.move_type != line.order_id.picking_policy:
                    updated_vals.update({'move_type': line.order_id.picking_policy})
                if updated_vals:
                    group_id.write(updated_vals)

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.product_uom_qty + line.free_qty - qty

            line_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
            procurements.append(self.env['procurement.group'].Procurement(
                line.product_id, product_qty, procurement_uom,
                line.order_id.partner_shipping_id.property_stock_customer,
                line.name, line.order_id.name, line.order_id.company_id, values))
        if procurements:
            self.env['procurement.group'].run(procurements)
        return True

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        self.ensure_one()
        res.update({
            'free_qty': self.free_qty_to_invoice,
        })
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    free_qty = fields.Float(string='Free Qty', digits='Product Unit of Measure', default=0.0)


