# -*- coding: utf-8 -*-
# from odoo import http


# class BrothersInvoicePrint(http.Controller):
#     @http.route('/brothers_invoice_print/brothers_invoice_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/brothers_invoice_print/brothers_invoice_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('brothers_invoice_print.listing', {
#             'root': '/brothers_invoice_print/brothers_invoice_print',
#             'objects': http.request.env['brothers_invoice_print.brothers_invoice_print'].search([]),
#         })

#     @http.route('/brothers_invoice_print/brothers_invoice_print/objects/<model("brothers_invoice_print.brothers_invoice_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('brothers_invoice_print.object', {
#             'object': obj
#         })
