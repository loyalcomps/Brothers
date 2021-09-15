# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

listedReasons = [
    ('1', 'Transhipment'),
    ('2', 'Vehicle Break down'),
    ('3', 'Not updated earlier')
]

class VehicleNoUpdation(models.TransientModel):
    _inherit = "vehicle.no.updation"

    def updateVehicleNo(self):

        ctx = dict(self._context or {})
        if ctx.get('sale_internal')=='internal':
            stockIds = ctx.get('active_ids')
            stockObjs = self.env['stock.picking'].search([('id', 'in', stockIds)])
            text = "Unable to update vehicle no"
            if stockObjs:
                vehicle_no = self.vehicle_no
                reason = self.reason
                remarks = self.remarks
                stockObjs.write({
                    'vehicle_no':vehicle_no,
                    'reason':reason,
                    'remarks':remarks,
                })
                reason = dict(listedReasons)[reason]
                text = "Vehicle No: <b>{}</b> for E-Way Bill Order <b>{}</b> has been successfully assigned.".format(vehicle_no, stockObjs.name)
                body = '{}<br/><b>Reason: </b>{} <br/><b>Remarks: </b>{}'.format(text, reason, remarks)
                stockObjs.message_post(body=_(body),subtype='mail.mt_comment')
            return self.env['wk.wizard.message'].genrated_message(text)
        else:
            res = super(VehicleNoUpdation, self).updateVehicleNo()
            return res

