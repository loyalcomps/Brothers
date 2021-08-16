# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def check_unique_mrp(self):
        result=[]
        mrp_duplicate = []
        mrp_float = []
        for product in self:
            mrp_values = self.env['stock.move.line'].search([('product_id','=',product.id)])
            mr = [rec.id for rec in mrp_values if rec.mrp != 0 and rec.mrp not in mrp_duplicate]
            serial_no = 1
            for rec in mrp_values:
                if rec.mrp != 0 and rec.mrp not in mrp_float:
                    rec.sl_no = serial_no
                    serial_no += 1
                    mrp_float.append(rec.mrp)
                    mrp_duplicate.append(rec.id)
            result = [('id', 'in', mrp_duplicate)]
            return result

    mrp_ids = fields.One2many(
        'stock.move.line',
        'product_id',
        string='MRP'
        ,domain=check_unique_mrp
    )
    # ,domain='_check_unique_mrp')
        # ,compute='_check_unique_mrp',inverse='inverse_check_unique_mrp')

    # @api.depends('mrp_ids', 'active', 'mrp_ids.mrp')


    # @api.depends('mrp_ids', 'active', 'mrp_ids.mrp')
    # # @api.onchange('mrp_ids', 'active')
    # def inverse_check_unique_mrp(self):
    #     mrp_duplicate = []
    #     # mrp_values = self.env['stock.move.line'].search([])
    #     for product in self:
    #         mrp_values = self.env['stock.move.line'].search([('product_id','=',product.id)])
    #
    #         for rec in self.mrp_ids:
    #             if rec.mrp not in mrp_duplicate:
    #                 mrp_duplicate.append((0, 0, {
    #                     'mrp': rec.mrp,
    #                 }))
    #     # self.mrp_ids = [(6, 0, [])]
    #     # self.mrp_ids = mrp_duplicate
    #         product.write({'mrp_ids': mrp_duplicate})
    #     return


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    mrp_ids = fields.One2many(related='product_variant_ids.mrp_ids',readonly=False)




