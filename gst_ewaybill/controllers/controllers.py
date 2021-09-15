# -*- coding: utf-8 -*-
# from odoo import http


# class GstEwaybill(http.Controller):
#     @http.route('/gst_ewaybill/gst_ewaybill/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gst_ewaybill/gst_ewaybill/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gst_ewaybill.listing', {
#             'root': '/gst_ewaybill/gst_ewaybill',
#             'objects': http.request.env['gst_ewaybill.gst_ewaybill'].search([]),
#         })

#     @http.route('/gst_ewaybill/gst_ewaybill/objects/<model("gst_ewaybill.gst_ewaybill"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gst_ewaybill.object', {
#             'object': obj
#         })
