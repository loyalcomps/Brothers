# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError
import base64
import json

listedReasons = [
    ('1', 'Transhipment'),
    ('2', 'Vehicle Break down'),
    ('3', 'Not updated earlier')
]

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    generate_ewaybill = fields.Boolean(
        string='Generate E-Way Bill',
        help="Enable to generate E-Way Bill"
    )
    transportation_distance = fields.Integer(
        string='Distance (Km)',
        help="Distance of transportation"
    )
    mainHsnCode = fields.Integer(
        string='Main HSN Code',
        help="HSN Code of the Product"
    )
    vehicle_no = fields.Char(
        string='Vehicle No',
        track_visibility='onchange',
        help="Vehicle No of transporter"
    )
    vehicle_type = fields.Selection(
        [
            ('R', 'Regular'),
            ('O', 'ODC')
        ],
        string='Vehicle Type',

    )
    supply_type = fields.Selection(
        [
            ('I', 'Inward'),
            ('O', 'Outward')
        ],
        string='Supply Type',
        help="Supply whether it is outward/inward."
    )
    sub_supply_type = fields.Selection(
        [
            ('1', 'Supply'),
            ('2', 'Import'),
            ('3', 'Export'),
            ('4', 'Job Work'),
            ('5', 'For Own Use'),
            ('6', 'Job work Returns'),
            ('7', 'Sales Return'),
            ('8', 'Others'),
            ('9', 'SKD/CKD'),
            ('10', 'Line Sales'),
            ('11', 'Recipient Not Known'),
            ('12', 'Exhibition or Fairs'),
        ],
        copy=False,
        string='Sub Supply Type',
        help="Sub types of Supply like supply, export, Job Work etc."
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
    transporter_id = fields.Many2one(
        "ewaybill.transporter",
        string='Transporter',
        ondelete='restrict',
        help="Select transporter for E-Way Bill"
    )
    trans_id = fields.Char(
        related='transporter_id.transporter_id',
        string='Transporter ID',
        help="""
                Transporter ID is a unique identification number allotted to transporters not registered under GST.
                Transporter ID consists of 15 digits.
                """
    )
    trans_type = fields.Selection(
        [
            ('1', 'Regular'),
            ('2', 'Bill To-Ship To'),
            ('3', 'Bill From-Dispatch From'),
            ('4', 'Combination of 2 and 3')
        ],
        string='Transaction Type',

    )
    ewaybill_no = fields.Char(
        string="E-Way Bill No",
        help="E-Way Bill Attachment"
    )
    eway_source = fields.Many2one(
        'res.country.state',
        # related='company_id.state_id',
        string='Source',
        store=True,
        help="Place of consignor"
    )
    eway_destination = fields.Many2one(
        'res.country.state',
        # related='company_id.state_id',
        string='Destination',
        store=True,
        help="Place of consignee"
    )
    reason = fields.Selection(
        listedReasons,
        string='Reason',
        help="Reasons to update vehicle-no"
    )
    remarks = fields.Text(
        string='Remarks',
        help="Remarks to update vehicle-no"
    )

    sub_supply_desc= fields.Char(
        string="Sub Supply Description",

    )

    @api.onchange('transporter_id')
    def onchangeTransporterId(self):
        if self.transporter_id:
            self.transportation_mode = self.transporter_id.transportation_mode

    def generateEWayBill(self):
        jsonAttachment = self.generateJson()
        if not jsonAttachment:
            raise UserError("JSON of E-Way Bill is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (jsonAttachment.id),
            'target': 'new',
        }

    def generateJson(self):
        stockIds = self._context.get('active_ids')
        stockObjs = self.search([('id', 'in', stockIds), ('generate_ewaybill', '=', True)])
        stockJsonList = []
        notewaylist = list(set(stockIds) - set(stockObjs.ids))
        for stockObj in stockObjs:
            partnerObj = stockObj.partner_id if stockObj.partner_id else stockObj.location_dest_id.company_id.partner_id
            currency = stockObj.currency_id
            amountTotal = stockObj.amount_untaxed
            totalamount = stockObj.amount_total
            if currency.name != 'INR':
                amountTotal = amountTotal * currency.rate
            transporterObj = stockObj.transporter_id
            orderLineData = stockObj.getStockOrderLineJson()
            sgstValue = orderLineData[0]
            igstValue = orderLineData[1]
            cgstValue = orderLineData[2]
            cessValue = orderLineData[3]
            itemdata = orderLineData[4]
            othercharge = orderLineData[5]

            totnonadvolvalue = 0
            # othercharge = 0

            orderJsonDate = stockObj.scheduled_date.strftime('%d/%m/%Y')
            transporterDate = transporterObj.transporter_date.strftime('%d/%m/%Y') if transporterObj.transporter_date else ""
            companyObj = stockObj.location_id.company_id.partner_id
            stockJsonData = {
                # 'genMode':'Excel',
                'userGstin': companyObj.vat or '',
                'supplyType': stockObj.supply_type or 'I',
                'subSupplyType': int(stockObj.sub_supply_type or 1),
                "subSupplyDesc": stockObj.sub_supply_desc or '',
                'docType': 'OTH',
                'docNo': stockObj.name or '',
                'docDate': orderJsonDate,
                'transType': stockObj.trans_type,
                'fromGstin': companyObj.vat or '',
                'fromTrdName': companyObj.name or '',
                'fromAddr1': companyObj.street or '',
                'fromAddr2': companyObj.street2 or '',
                'fromPlace': companyObj.city or '',
                'fromPincode': int(companyObj.zip or 0),
                'fromStateCode': int(companyObj.state_id.l10n_in_tin or 32),
                'actualFromStateCode': int(companyObj.state_id.l10n_in_tin or 0),
                'toGstin': partnerObj.vat or '',
                'toTrdName': partnerObj.name or '',
                'toAddr1': partnerObj.street or '',
                'toAddr2': partnerObj.street2 or '',
                'toPlace': partnerObj.city or '',
                'toPincode': int(partnerObj.zip or 0),
                'toStateCode': int(partnerObj.state_id.l10n_in_tin or 0),
                'actualToStateCode': int(partnerObj.state_id.l10n_in_tin or 0),
                'totalValue': round(amountTotal, 3),
                'cgstValue': cgstValue,
                'sgstValue': sgstValue,
                'igstValue': igstValue,
                'cessValue': cessValue,
                # 'TotNonAdvolVal': totnonadvolvalue,
                'OthValue': othercharge,
                # 'totInvValue':round((amountTotal+sgstValue+cgstValue+igstValue+cessValue),2),
                'totInvValue': totalamount,
                'transMode': int(stockObj.transportation_mode),
                'transDistance': int(stockObj.transportation_distance or 0),
                'transporterName': transporterObj.name or '',
                'transporterId': transporterObj.transporter_id or '',
                'transDocNo': transporterObj.transporter_doc_no or '',
                'transDocDate': transporterDate,
                'vehicleNo': stockObj.vehicle_no or '',
                'vehicleType': stockObj.vehicle_type,
                'mainHsnCode': stockObj.mainHsnCode,
                'itemList': itemdata,

            }
            stockJsonList.append(stockJsonData)
        jsonData = {
            'version': '1.0.0421',
            'billLists': stockJsonList
        }
        jsonAttachment = self.generatejsonAttachment(jsonData, "ewaybillgst.json")
        return jsonAttachment

    def generatejsonAttachment(self, jsonData, jsonFileName):
        jsonAttachment = False
        if jsonData:
            jsonData = json.dumps(jsonData, indent=4, sort_keys=False)
            base64Data = base64.b64encode(jsonData.encode('utf-8'))
            try:
                ewaydata = {
                    'datas': base64Data,
                    'type': 'binary',
                    'res_model': 'stock.picking',
                    'res_id': False,
                    # 'db_datas': jsonFileName,
                    # 'datas_fname': jsonFileName,
                    'name': jsonFileName
                }
                jsonObjs = self.env['ir.attachment'].search([('name', '=', jsonFileName)])
                if jsonObjs:
                    jsonAttachment = jsonObjs[0]
                    jsonAttachment.write(ewaydata)
                else:
                    jsonAttachment = self.env['ir.attachment'].create(ewaydata)
            except ValueError:
                pass
        return jsonAttachment


    def getStockOrderLineJson(self):
        itemList = []
        itemNo = 1
        sgstRateAmount, igstRateAmount, cgstRateAmount, cessRateAmount, kfcRateAmount = 0.0, 0.0, 0.0, 0.0, 0.0
        for lineObj in self.move_line_ids_without_package:
            productObj = lineObj.product_id
            productName = productObj.name
            taxedAmount = lineObj.price_tax
            uqc = 'OTH'
            if lineObj.product_uom_id:
                uom = lineObj.product_uom_id.id
                uqcObj = self.env['ewaybill.uqc'].search([('uom', '=', uom)])
                if uqcObj:
                    uqc = uqcObj[0].code
            hsnCode = productObj.l10n_in_hsn_code or 0
            hsnCode = int(hsnCode)
            itemDict = {
                'itemNo': itemNo,
                'productName': productName,
                'productDesc': productName,
                'hsnCode': hsnCode,
                'quantity': lineObj.qty_done,
                'qtyUnit': uqc,
                'taxableAmount': lineObj.price_subtotal,
                'sgstRate': 0,
                'cgstRate': 0,
                'igstRate': 0,
                'cessRate': 0,
                # 'cessNonAdvol': 0,
            }
            if lineObj.taxes_id:
                partner_id = lineObj.picking_id.partner_id if lineObj.picking_id.partner_id else lineObj.picking_id.location_id.company_id.partner_id
                line_taxes = lineObj.taxes_id.compute_all(lineObj.price_unit, lineObj.picking_id.currency_id,
                                                          lineObj.qty_done,
                                                          product=lineObj.product_id, partner=partner_id)
                for tax_line in line_taxes['taxes']:
                    if 'IGST' in tax_line['name']:
                        cgstRateAmount += tax_line['amount'] / 2
                        sgstRateAmount += tax_line['amount'] / 2
                        # igstRateAmount += tax_line['amount']
                    elif 'CGST' in tax_line['name']:
                        cgstRateAmount += tax_line['amount']
                    elif 'SGST' in tax_line['name'] or 'UTGST' in tax_line['name']:
                        sgstRateAmount += tax_line['amount']
                    elif 'kfc' in tax_line['name'].lower():
                        kfcRateAmount += tax_line['amount']
                    else:
                        cessRateAmount += tax_line['amount']
                for rateObj in lineObj.taxes_id:
                    if rateObj.amount_type == "group":

                        for childObj in rateObj.children_tax_ids:
                            if 'CGST' in childObj.name:
                                itemDict['cgstRate'] += childObj.amount
                            elif 'SGST' in childObj.name:
                                itemDict['sgstRate'] += childObj.amount
                            else:
                                itemDict['cessRate'] += childObj.amount

                            # sgstRateAmount = sgstRateAmount + taxedAmount / 2

                    else:
                        itemDict['cgstRate'] += rateObj.amount / 2
                        itemDict['sgstRate'] += rateObj.amount / 2
                        # itemDict['igstRate'] += rateObj.amount
                        # igstRateAmount = igstRateAmount + taxedAmount
                    break
            itemList.append(itemDict)
            itemNo = itemNo + 1
        sgstRateAmount = round(sgstRateAmount, 2)
        igstRateAmount = igstRateAmount
        cgstRateAmount = round(cgstRateAmount, 2)
        kfcRateAmount = round(kfcRateAmount, 2)
        cessRateAmount = round(cessRateAmount, 2)
        return [sgstRateAmount, igstRateAmount, cgstRateAmount, cessRateAmount, itemList, kfcRateAmount]


    def updateVehicleNo(self):
        partial = self.env['vehicle.no.updation'].create({
            'vehicle_no': self.vehicle_no
        })
        return {'name': ("Update Vehicle No."),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'vehicle.no.updation',
                'res_id': partial.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': self._context,
                'domain': '[]',
                }


    def generateVehicleUpdateJson(self):
        jsonAttachment = self.generateVehicleJson()
        if not jsonAttachment:
            return self.env['wk.wizard.message'].genrated_message(
                "<h3 style='color: #d9534f;'>E-Way Bills are not generated for selected internal transfer</h3>")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (jsonAttachment.id),
            'target': 'new',
        }

    def generateVehicleJson(self):
        saleIds = self._context.get('active_ids')
        saleObjs = self.search([('id', 'in', saleIds), ('generate_ewaybill', '=', True), ('ewaybill_no', '!=', '')])

        jsonAttachment = False
        if not saleObjs:
            return False
        else:
            vehicleUpdateList = []
            for saleObj in saleObjs:
                transporterObj = saleObj.transporter_id
                companyObj = saleObj.company_id
                transporterDate = transporterObj.transporter_date.strftime('%d/%m/%Y')
                vehicleUpdateJson = {
                    "ewbno": int(saleObj.ewaybill_no),
                    "transMode": int(saleObj.transportation_mode),
                    "vehicleType": saleObj.vehicle_type or '',
                    "vehicleNo": saleObj.vehicle_no or '',
                    "docNo": transporterObj.transporter_doc_no,
                    "docDate": transporterDate,
                    'fromPlace': companyObj.city or '',
                    'fromState': int(companyObj.state_id.l10n_in_tin or 32),
                    "reason": int(saleObj.reason),
                    "remark": saleObj.remarks or ''
                }
                vehicleUpdateList.append(vehicleUpdateJson)
            jsonData = {
                'version': '1.0.0123',
                'userGstin': self.env.user.company_id.vat or '',
                'vehicleUpdts': vehicleUpdateList
            }
            jsonAttachment = self.generatejsonAttachment(jsonData, "vehicleUpdate.json")
        return jsonAttachment


    def generateTransporterUpdateJson(self):
        jsonAttachment = self.generateTransporterJson()
        if not jsonAttachment:
            raise UserError("Transporter is not selected for selected internal transfer")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (jsonAttachment.id),
            'target': 'new',
        }

    def generateTransporterJson(self):
        stockIds = self._context.get('active_ids')
        stockObjs = self.search([('id', 'in', stockIds), ('generate_ewaybill', '=', True), ('ewaybill_no', '!=', ''),
                                 ('trans_id', '!=', '')])
        jsonAttachment = False
        if not stockObjs:
            return False
        else:
            transUpdateList = []
            for stockObj in stockObjs:
                transUpdateJson = {
                    "ewaybillNo": int(stockObj.ewaybill_no),
                    "TransporterId": stockObj.trans_id,

                }
                transUpdateList.append(transUpdateJson)
            jsonData = {
                'version': '1.0.0123',
                'userGstin': self.env.user.company_id.vat or '',
                'TransUpdts': transUpdateList
            }
            jsonAttachment = self.generatejsonAttachment(jsonData, "transporterUpdate.json")
        return jsonAttachment
