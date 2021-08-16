# -*- coding: utf-8 -*-
# from odoo import http


# class ProductLotMrp(http.Controller):
#     @http.route('/product_lot_mrp/product_lot_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_lot_mrp/product_lot_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_lot_mrp.listing', {
#             'root': '/product_lot_mrp/product_lot_mrp',
#             'objects': http.request.env['product_lot_mrp.product_lot_mrp'].search([]),
#         })

#     @http.route('/product_lot_mrp/product_lot_mrp/objects/<model("product_lot_mrp.product_lot_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_lot_mrp.object', {
#             'object': obj
#         })
