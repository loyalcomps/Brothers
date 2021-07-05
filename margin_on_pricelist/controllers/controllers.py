# -*- coding: utf-8 -*-
# from odoo import http


# class MarginOnPricelist(http.Controller):
#     @http.route('/margin_on_pricelist/margin_on_pricelist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/margin_on_pricelist/margin_on_pricelist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('margin_on_pricelist.listing', {
#             'root': '/margin_on_pricelist/margin_on_pricelist',
#             'objects': http.request.env['margin_on_pricelist.margin_on_pricelist'].search([]),
#         })

#     @http.route('/margin_on_pricelist/margin_on_pricelist/objects/<model("margin_on_pricelist.margin_on_pricelist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('margin_on_pricelist.object', {
#             'object': obj
#         })
