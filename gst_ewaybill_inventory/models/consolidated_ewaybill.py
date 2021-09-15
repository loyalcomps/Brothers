# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError

class ConsolidatedEwaybill(models.TransientModel):
    _inherit = "consolidated.ewaybill"

    ewaybill_stock_ids = fields.Many2many(
        'stock.picking',
        # 'order_ewaybill_set',
        # 'order_id',
        # 'attribute_id',
        string='E-Way Bill Orders',
        help="E-way Bill Approved Orders."
    )

    intrnl_trans = fields.Boolean(default=False)

    def consolidatedEwaybillInternalTrans(self):
        ctx = dict(self._context or {})
        saleIds = ctx.get('active_ids')
        saleObjs = self.env['stock.picking'].search(
            [('id', 'in', saleIds), ('ewaybill_no', '!=', ''), ('generate_ewaybill', '=', True)])
        partial = self.create({
            'ewaybill_stock_ids': [(6, 0, saleObjs.ids)],
            'intrnl_trans': True
        })
        view_id = self.env.ref('gst_ewaybill_inventory.consolidated_ewaybill_form_internal_trans')
        return {'name': ("Consolidated E-Way Bill"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'consolidated.ewaybill',
                'res_id': partial.id,

                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': ctx,
                'domain': '[]',
                }


    def printBillInternalTrans(self):
        jsonAttachment = self.generateJsonIntrnlTrans()
        if not jsonAttachment:
            raise UserError("Consolidated JSON of E-Way Bill is not present")
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=1' % (jsonAttachment.id),
            'target': 'new',
        }

    def generateJsonIntrnlTrans(self):

        ewaybillOrderNos = self.ewaybill_stock_ids.mapped('ewaybill_no')
        tripSheetEwbBills = []
        for ewaybillOrderNo in ewaybillOrderNos:
            tripSheetEwbBills.append({'ewbno': int(ewaybillOrderNo or 0)})
        transObj = self.transporter_id
        transporterDate = transObj.transporter_date.strftime('%d/%m/%Y')
        consolidateJson = {
            "userGstin": self.company_id.vat or '',
            # "userGstin":self.trans_id or '',
            "vehicleNo": self.vehicle_no or '',
            "transDocNo": transObj.transporter_doc_no or '',
            "transDocDate": transporterDate or '',
            "fromPlace": self.city or '',
            "transMode": self.transportation_mode or '',
            "fromState": self.state_id.l10n_in_tin or '',
            "tripSheetEwbBills": tripSheetEwbBills or ''
        }
        jsonData = {
            'version': '1.0.0618',

            'tripSheets': [consolidateJson]
        }
        jsonAttachment = self.env['stock.picking'].generatejsonAttachment(jsonData, "consolidatedEwaybillgst.json")
        return jsonAttachment
