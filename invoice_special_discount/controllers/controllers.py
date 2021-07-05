# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceSpecialDiscount(http.Controller):
#     @http.route('/invoice_special_discount/invoice_special_discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_special_discount/invoice_special_discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_special_discount.listing', {
#             'root': '/invoice_special_discount/invoice_special_discount',
#             'objects': http.request.env['invoice_special_discount.invoice_special_discount'].search([]),
#         })

#     @http.route('/invoice_special_discount/invoice_special_discount/objects/<model("invoice_special_discount.invoice_special_discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_special_discount.object', {
#             'object': obj
#         })
