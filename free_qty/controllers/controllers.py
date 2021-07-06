# -*- coding: utf-8 -*-
# from odoo import http


# class FreeQty(http.Controller):
#     @http.route('/free_qty/free_qty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/free_qty/free_qty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('free_qty.listing', {
#             'root': '/free_qty/free_qty',
#             'objects': http.request.env['free_qty.free_qty'].search([]),
#         })

#     @http.route('/free_qty/free_qty/objects/<model("free_qty.free_qty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('free_qty.object', {
#             'object': obj
#         })
