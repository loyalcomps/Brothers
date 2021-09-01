# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def check_unique_stock_mrp(self):
        result=[]
        mrp_duplicate = []
        mrp_float = []
        for product in self:
            mrp_values = self.env['stock.mrp.product.report'].search([('product_id','=',product.id)])
            mr = [rec.id for rec in mrp_values if rec.mrp != 0 and rec.mrp not in mrp_duplicate]
            serial_no = 1
            for rec in mrp_values:
                if rec.mrp != 0 and rec.mrp not in mrp_float:
                    rec.sl_no = serial_no
                    serial_no += 1
                    mrp_float.append(rec.mrp)
                    mrp_duplicate.append(rec.id)
            result = [('id', 'in', mrp_duplicate)]
            return [('id', 'in', mrp_duplicate)]

    product_mrp_ids = fields.One2many(
        'stock.mrp.product.report',
        'product_id',
        string='MRP'
        ,domain=check_unique_stock_mrp
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_mrp_ids = fields.One2many(related='product_variant_ids.product_mrp_ids',readonly=False)




