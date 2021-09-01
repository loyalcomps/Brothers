# -*- coding: utf-8 -*-
# from odoo import http


# class ProductMrp(http.Controller):
#     @http.route('/product_mrp/product_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_mrp/product_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_mrp.listing', {
#             'root': '/product_mrp/product_mrp',
#             'objects': http.request.env['product_mrp.product_mrp'].search([]),
#         })

#     @http.route('/product_mrp/product_mrp/objects/<model("product_mrp.product_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_mrp.object', {
#             'object': obj
#         })
