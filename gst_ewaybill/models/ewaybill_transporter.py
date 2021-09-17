# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class EwaybillTransporter(models.Model):
    _name = "ewaybill.transporter"
    _inherit = ['mail.thread']
    _description = 'Eway Bill Transporter'

    name = fields.Char(
        string='Transporter Name',
        help="Transporter Name"
    )
    transportation_mode = fields.Selection(
        [
            ('1', 'Road'),
            ('2', 'Rail'),
            ('3', 'Air'),
            ('4', 'Ship')
        ],
        string='Transportation Mode',
        help="""
        Mode of transport is a term used to distinguish substantially different ways to perform.
        The different modes of transport are air, road, rail and ship transport.
        """
    )
    transporter_id = fields.Char(
        string='Transporter ID',
        help="""
        Transporter ID is a unique identification number allotted to transporters not registered under GST.
        Transporter ID consists of 15 digits.
        """
    )
    transporter_doc_no = fields.Char(
        string='Document Number',
        help="""
        Goods Receipt Number or Railway Receipt Number or Airway Bill Number or Bill of Lading Number.
        """
    )
    transporter_date = fields.Date(
        string='Document Date',
        required=True,
        index=True,
        default=fields.Datetime.now,
        help="Transporter document date"
    )
    mobile_no = fields.Char(
        string='Mobile No.',
        help="Mobile No of Transporter"
    )
    email_id = fields.Char(
        string='Email-ID',
        help="Email-ID of Transporter"
    )
    transporter_address1 = fields.Char(
        string='Street 1',
        help="Address of consignee - Line 1"
    )
    transporter_address2 = fields.Char(
        string='Street 2',
        help="Address of consignee - Line 2"
    )
    city = fields.Char(
        string="Place",
        help="Place of consignee"
    )
    zip = fields.Char(
        string="Pincode",
        change_default=True,
        help="Pincode of the consignee"
    )
    state_id = fields.Many2one(
        "res.country.state",
        string='State',
        ondelete='restrict',
        help="State of Supply"
    )
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        ondelete='restrict',
        help="Country of Supply"
    )
