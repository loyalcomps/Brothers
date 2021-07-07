# -*- coding: utf-8 -*-
# from odoo import http


# class SalePriceListExtraDiscount(http.Controller):
#     @http.route('/sale_price_list_extra_discount/sale_price_list_extra_discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_price_list_extra_discount/sale_price_list_extra_discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_price_list_extra_discount.listing', {
#             'root': '/sale_price_list_extra_discount/sale_price_list_extra_discount',
#             'objects': http.request.env['sale_price_list_extra_discount.sale_price_list_extra_discount'].search([]),
#         })

#     @http.route('/sale_price_list_extra_discount/sale_price_list_extra_discount/objects/<model("sale_price_list_extra_discount.sale_price_list_extra_discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_price_list_extra_discount.object', {
#             'object': obj
#         })
