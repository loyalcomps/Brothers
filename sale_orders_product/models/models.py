# -*- coding: utf-8 -*-

from ast import literal_eval

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def mobile_action_fsm_view_material(self):
        if not self.partner_id:
            raise UserError(_('A customer should be set on the Sale Order to generate a Order.'))

        self = self.with_company(self.company_id)

        domain = [('sale_ok', '=', True), '|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)]
        kanban_view = self.env.ref('sale_orders_product.product_sale_orders_kanban_view')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choose Products'),
            'res_model': 'product.product',
            'search_view_id': [self.env.ref('sale_orders_product.mrp_product_template_search_view').id, 'search'],

            'views': [(kanban_view.id, 'kanban'), (False, 'form')],
            'domain': domain,
            'context': {
                'fsm_mode': True,
                'create': self.env['product.template'].check_access_rights('create', raise_exception=False),
                'fsm_sale_id': self.id,  # avoid 'default_' context key as we are going to create SOL with this context
                'pricelist': self.pricelist_id.id,
                # self.partner_id.property_product_pricelist.id,
                'search_default_consumable': 1,
                'hide_qty_buttons': self.state == 'done'
            },
            'help': _("""<p class="o_view_nocontent_smiling_face">
                               Create a new product
                           </p><p>
                               You must define a product for everything you sell or purchase,
                               whether it's a storable product, a consumable or a service.
                           </p>""")
        }