# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    mrp = fields.Float(string='MRP', digits='Product Price', default=0.0)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    mrp = fields.Float(string='MRP', digits='Product Price', related='lot_id.mrp', store=True, readonly=False)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    mrp = fields.Float(string='MRP', digits='Product Price', related='lot_id.mrp', store=True, readonly=False)

