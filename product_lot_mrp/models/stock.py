# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sl_no = fields.Integer(string='Sl No.',store=True)

    # @api.depends('move_id', 'move_id.move_line_nosuggest_ids')
    # def _get_line_numbers(self):
    #     line_num = 1
    #     for order_line in self:
    #         if not order_line.sl_no:
    #             serial_no = 1
    #             for line in order_line.mapped('move_id').move_line_nosuggest_ids:
    #                 line.sl_no = serial_no
    #                 serial_no += 1
        # line_num = 1
        # if self.ids:
        #     first_line_rec = self.browse(self.ids[0])

            # for line_rec in first_line_rec.move_id.move_line_ids:
            #     line_rec.sl_no = line_num
            #     line_num += 1
