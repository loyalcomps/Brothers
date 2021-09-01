# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sl_no = fields.Integer(string='Sl No.',store=True)

