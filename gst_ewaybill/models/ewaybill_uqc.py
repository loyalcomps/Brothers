# -*- coding: utf-8 -*-

from odoo import api, fields, models

class EwaybillUqc(models.Model):
    _name = "ewaybill.uqc"
    _description = "Ewaybill UQC"

    name = fields.Char(
        string="Unit",
        help="UQC (Unit of Measure) of goods sold"
    )
    code = fields.Char(
        string="Code",
        help="Code for UQC (Unit of Measure)"
    )
    uom = fields.Many2one(
        "uom.uom",
        string="Units of Measure",
        help="Units of Measure use for all stock operation"
    )