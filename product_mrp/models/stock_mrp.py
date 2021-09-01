# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models

class ProductMRPReport(models.Model):
    _name = "stock.mrp.product.report"
    _description = "Product MRP"
    _auto = False
    _rec_name = "name"
    _order = "id"

    name = fields.Char(string='MRP')
    sl_no = fields.Integer(string='sl')
    product_id = fields.Many2one('product.product',string='product')
    move_id = fields.Many2one('stock.move',string="Move")
    company_id = fields.Many2one('res.company', string='Company')
    mrp = fields.Float(string='MRP',default=0.0)


    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            SELECT  a.id as id,
                a.sl_no as sl_no,
                a.move_id,
                a.company_id,
                a.product_id,
                a.mrp,
                cast(a.mrp as text) as name
            FROM stock_move_line a            
            )''' % (self._table,)
        )


    #
    # def _query(self, fields='', from_clause=''):
    #     select_ = """
    #             a.id as id,
    #             1 as sl_no,
    #             a.move_id,
    #             a.company_id,
    #             a.product_id,
    #             a.mrp,
    #             cast(a.mrp as text) as name
    #             %s
    #     """ % fields
    #
    #     from_ = """
    #             stock_move_line a
    #             %s
    #     """ % from_clause
    #
    #     return '(SELECT %s FROM %s)' % (select_, from_)
    #
    # def init(self):
    #     tools.drop_view_if_exists(self.env.cr, self._table)
    #     self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

