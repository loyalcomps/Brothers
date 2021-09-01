# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrdersProduct(http.Controller):
#     @http.route('/sale_orders_product/sale_orders_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_orders_product/sale_orders_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_orders_product.listing', {
#             'root': '/sale_orders_product/sale_orders_product',
#             'objects': http.request.env['sale_orders_product.sale_orders_product'].search([]),
#         })

#     @http.route('/sale_orders_product/sale_orders_product/objects/<model("sale_orders_product.sale_orders_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_orders_product.object', {
#             'object': obj
#         })
