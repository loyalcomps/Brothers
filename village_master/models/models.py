# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VillageMaster(models.Model):
    _name = 'village.master'
    _description = 'Village master'

    name = fields.Char()


class Partner(models.Model):
    _inherit = 'res.partner'

    village_id = fields.Many2one('village.master', string='Village')

