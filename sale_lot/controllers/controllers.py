# -*- coding: utf-8 -*-
# from odoo import http


# class SaleLot(http.Controller):
#     @http.route('/sale_lot/sale_lot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_lot/sale_lot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_lot.listing', {
#             'root': '/sale_lot/sale_lot',
#             'objects': http.request.env['sale_lot.sale_lot'].search([]),
#         })

#     @http.route('/sale_lot/sale_lot/objects/<model("sale_lot.sale_lot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_lot.object', {
#             'object': obj
#         })
