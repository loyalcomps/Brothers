# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict

from odoo import api, fields, models,_


class ProductProduct(models.Model):
    _inherit = 'product.product'

    mobile_fsm_quantity = fields.Float('Material Quantity', compute="_compute_mobile_fsm_quantity", inverse="_inverse_mobile_fsm_quantity")
    mobile_fsm_free_quantity = fields.Float('Free Quantity', compute="_compute_mobile_fsm_quantity", inverse="_inverse_mobile_fsm_quantity")
    mobile_fsm_mrp = fields.Many2one('stock.mrp.product.report',string='MRP Value', compute="_compute_mobile_fsm_quantity", inverse="_inverse_mobile_fsm_quantity")
    mobile_mrp_value = fields.Float('Free Quantity')

    sale_note = fields.Char('Mobile Note')

    def mobile_note(self):
        action = self.env.ref(
            'sale_orders_product.action_form_for_note').read()[0]
        action['context'] = {
            'default_res_model': self._name,
            'default_res_id': self.ids[0],
            'fsm_sale_id': self.env.context.get('fsm_sale_id'),
            'fsm_product_id':self.id
        }
        return action

    def mobile_mrp_view(self):
        action = self.env.ref(
            'sale_orders_product.action_form_for_mrp').read()[0]
        action['context'] = {
            'default_res_model': self._name,
            'default_res_id': self.ids[0],
            'fsm_sale_id': self.env.context.get('fsm_sale_id'),
            'fsm_product_id':self.id,
            'default_product_id': self.id,
            # 'product_mrp':self.mobile_fsm_mrp.id,
        }
        return action

    @api.depends_context('fsm_sale_id')
    def _compute_mobile_fsm_quantity(self):
        sale = self._get_contextual_mobile_fsm_task()
        if sale:

            SaleOrderLine = self.env['sale.order.line']
            if self.user_has_groups('sales_team.group_sale_salesman'):
                sale = sale.sudo()
                SaleOrderLine = SaleOrderLine.sudo()

            products_qties = SaleOrderLine.read_group(
                [('id', 'in', sale.order_line.ids)],
                ['product_id', 'product_uom_qty'], ['product_id'])
            products_free_qties = SaleOrderLine.read_group(
                [('id', 'in', sale.order_line.ids)],
                ['product_id', 'free_qty'], ['product_id'])
            qty_dict = dict([(x['product_id'][0], x['product_uom_qty']) for x in products_qties if x['product_id']])
            free_qty_dict = dict([(x['product_id'][0], x['free_qty']) for x in products_free_qties if x['product_id']])

            for product in self:
                product.mobile_fsm_quantity = qty_dict.get(product.id, 0)
                product.mobile_fsm_free_quantity = free_qty_dict.get(product.id, 0)
        else:
            self.mobile_fsm_quantity = False
            self.mobile_fsm_free_quantity = False

    def _inverse_mobile_fsm_quantity(self):
        sale = self._get_contextual_mobile_fsm_task()
        if sale:
            for product in self:
                sale_line = self.env['sale.order.line'].search([('order_id', '=', sale.id), ('product_id', '=', product.id), '|', '|', ('qty_delivered', '=', 0.0), ('qty_delivered_method', '=', 'manual'), ('state', 'not in', ['sale', 'done'])], limit=1)
                if sale_line:  # existing line: change ordered qty (and delivered, if delivered method)
                    vals = {
                        'product_uom_qty': product.mobile_fsm_quantity,
                        'free_qty':product.mobile_fsm_free_quantity
                    }
                    if sale_line.qty_delivered_method == 'manual':
                        vals['qty_delivered'] = product.mobile_fsm_quantity
                        vals['free_qty'] = product.mobile_fsm_free_quantity
                    sale_line.with_context(fsm_no_message_post=True).write(vals)
                else:  # create new SOL
                    vals = {
                        'order_id': sale.id,
                        'product_id': product.id,
                        'product_uom_qty': product.mobile_fsm_quantity,
                        'product_uom': product.uom_id.id,
                        'free_qty':product.mobile_fsm_free_quantity,
                    }
                    if product.service_type == 'manual':
                        vals['qty_delivered'] = product.mobile_fsm_quantity
                        vals['free_qty'] = product.mobile_fsm_free_quantity

                    if sale.pricelist_id.discount_policy == 'without_discount':
                        sol = self.env['sale.order.line'].new(vals)
                        sol._onchange_discount()
                        vals.update({'discount': sol.discount or 0.0})
                    sale_line = self.env['sale.order.line'].create(vals)

    @api.model
    def _get_contextual_mobile_fsm_task(self):
        sale_id = self.env.context.get('fsm_sale_id')
        if sale_id:
            return self.env['sale.order'].browse(sale_id)
        return self.env['sale.order']

    def set_mobile_fsm_quantity(self, quantity):
        sale = self._get_contextual_mobile_fsm_task()
        # project user with no sale rights should be able to change material quantities
        if not sale or quantity and quantity < 0 or not self.user_has_groups('sales_team.group_sale_salesman'):
            return
        self = self.sudo()
        # don't add material on confirmed/locked SO to avoid inconsistence with the stock picking
        if sale.state == 'done':
            return False
        # ensure that the task is linked to a sale order
        # wizard_product_lot = self.action_assign_serial()
        # if wizard_product_lot:
        #     return wizard_product_lot
        self.mobile_fsm_quantity = quantity
        return True


    def set_mobile_fsm_free_quantity(self, quantity):
        sale = self._get_contextual_mobile_fsm_task()
        # project user with no sale rights should be able to change material quantities
        if not sale or quantity and quantity < 0 or not self.user_has_groups('sales_team.group_sale_salesman'):
            return
        self = self.sudo()
        # don't add material on confirmed/locked SO to avoid inconsistence with the stock picking
        if sale.state == 'done':
            return False
        # ensure that the task is linked to a sale order

        self.mobile_fsm_free_quantity = quantity
        return True


    # Is override by fsm_stock to manage lot
    def action_assign_serial(self):
        return False

    def mobile_fsm_add_quantity(self):
        return self.set_mobile_fsm_quantity(self.sudo().mobile_fsm_quantity + 1)

    def mobile_fsm_remove_quantity(self):
        return self.set_mobile_fsm_quantity(self.sudo().mobile_fsm_quantity - 1)

    def mobile_fsm_free_add_quantity(self):
        return self.set_mobile_fsm_free_quantity(self.sudo().mobile_fsm_free_quantity + 1)

    def mobile_fsm_free_remove_quantity(self):
        return self.set_mobile_fsm_free_quantity(self.sudo().mobile_fsm_free_quantity - 1)


class SaleLineNote(models.TransientModel):
    _name = 'sale.line.note'

    # @api.depends('product_id')
    # @api.depends_context('fsm_sale_id', 'show_mrp')
    def _compute_get_lot_mrps(self):
        mrp_float = []
        order = self.env['product.product'].browse(self._context.get('fsm_product_id'))
        for product in order:
            lot_mrp = product.product_mrp_ids
            if lot_mrp:
                for rec in lot_mrp:
                    mrp_float.append(rec.id)

        res = {}
        res['domain'] = {'mrp_value': [('id', 'in', mrp_float)]}
        return [('id', 'in', mrp_float)]

    sale_note = fields.Char(string="Note",store=True)
    sale_id = fields.Many2one('sale.order', string='Sale Order',store=True)
    product_id = fields.Many2one('product.product', string='Product',store=True)
    mrp_value = fields.Many2one('stock.mrp.product.report',string='MRP',store=True,domain=_compute_get_lot_mrps)


    @api.model
    def _prepare_default_get(self, order):
        default = {
            'sale_id': self._context.get('fsm_sale_id'),
            'sale_note':order.sale_note,
            'product_id':order.id,
            'mrp_value':order.mobile_fsm_mrp.id,

        }
        return default

    @api.model
    def default_get(self, fields):
        res = super(SaleLineNote, self).default_get(fields)
        assert self._context.get('active_model') == 'product.product', \
            'active_model should be product.product'
        sale = self._context.get('fsm_sale_id')
        sale_order = self.env['sale.order'].browse(sale)
        order = self.env['product.product'].browse(self._context.get('active_id'))
        default = self._prepare_default_get(order)
        self._compute_get_lot_mrps()
        res.update(default)
        return res


    @api.model
    def _get_contextual_mobile_fsm_task(self):
        sale_id = self.env.context.get('fsm_sale_id')
        if sale_id:
            return self.env['sale.order'].browse(sale_id)
        return self.env['sale.order']

    def confirm(self):
        self.ensure_one()
        # confirm sale order
        sale_order = self.env['sale.order'].browse(self._context.get('fsm_sale_id'))
        sale = self._get_contextual_mobile_fsm_task()
        if sale:
            for product in self:
                # sale_line = self.env['sale.order.line'].search(
                #     [('order_id', '=', sale.id), '|', '|', ('qty_delivered', '=', 0.0),
                #      ('qty_delivered_method', '=', 'manual'), ('state', 'not in', ['sale', 'done'])], limit=1)
                # if sale_line:  # existing line: change ordered qty (and delivered, if delivered method)
                vals = {
                        'name': self.sale_note,
                        'order_id': sale.id,
                        'display_type': 'line_note',
                        'product_id': False,
                        'product_uom_qty': 0,
                        'product_uom': False,
                        'price_unit': 0,
                        'tax_id': False,
                    }

                sale_line = self.env['sale.order.line'].create(vals)
        # vals = self._prepare_update_so()
        # self.sale_id.write(vals)
        return True

    def add_mrp_button(self):
        sale = self._get_contextual_mobile_fsm_task()
        if sale:
            for product in self:
                sale_line = self.env['sale.order.line'].search([('order_id', '=', sale.id), ('product_id', '=', product.product_id.id), '|', '|', ('qty_delivered', '=', 0.0), ('qty_delivered_method', '=', 'manual'), ('state', 'not in', ['sale', 'done'])], limit=1)
                if product.mrp_value:
                    product.product_id.with_context(
                        product_mrp=product.mrp_value.id
                    ).mobile_mrp_value = product.mrp_value.mrp
                if sale_line:  # existing line: change ordered qty (and delivered, if delivered method)

                    # mobile_mrp_value
                    vals = {
                        'product_mrp': product.mrp_value.id,
                        'qty_available': product.product_id.qty_available
                    }
                    if sale_line.qty_delivered_method == 'manual':
                        vals['product_mrp'] = product.mrp_value.id
                        vals['qty_available'] = product.product_id.qty_available
                    product.product_id.with_context(
                        product_mrp=product.mrp_value.id
                    )
                    sale_line.with_context(fsm_no_message_post=True,product_mrp=product.mrp_value.id).write(vals)

                    sale_line.product_mrp_change()
                else:  # create new SOL
                    vals = {
                        'order_id': sale.id,
                        'product_id': product.product_id.id,
                        # 'product_uom_qty': product.mobile_fsm_quantity,
                        'product_uom': product.product_id.uom_id.id,
                        'product_mrp': product.mrp_value.id,
                        'qty_available':product.product_id.qty_available
                    }
                    if product.product_id.service_type == 'manual':
                        vals['product_mrp'] = product.mrp_value.id
                    if sale.pricelist_id.discount_policy == 'without_discount':
                        sol = self.env['sale.order.line'].new(vals)
                        sol._onchange_discount()
                        vals.update({'discount': sol.discount or 0.0})

                    sale_line = self.env['sale.order.line'].with_context(
                        product_mrp=product.mrp_value.id
                    ).create(vals)
                    sale_line.product_mrp_change()

