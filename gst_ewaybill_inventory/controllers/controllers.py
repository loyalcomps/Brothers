# -*- coding: utf-8 -*-
# from odoo import http


# class GstEwaybillInventory(http.Controller):
#     @http.route('/gst_ewaybill_inventory/gst_ewaybill_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gst_ewaybill_inventory/gst_ewaybill_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gst_ewaybill_inventory.listing', {
#             'root': '/gst_ewaybill_inventory/gst_ewaybill_inventory',
#             'objects': http.request.env['gst_ewaybill_inventory.gst_ewaybill_inventory'].search([]),
#         })

#     @http.route('/gst_ewaybill_inventory/gst_ewaybill_inventory/objects/<model("gst_ewaybill_inventory.gst_ewaybill_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gst_ewaybill_inventory.object', {
#             'object': obj
#         })
