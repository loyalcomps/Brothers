# -*- coding: utf-8 -*-
# from odoo import http


# class VillageMaster(http.Controller):
#     @http.route('/village_master/village_master/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/village_master/village_master/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('village_master.listing', {
#             'root': '/village_master/village_master',
#             'objects': http.request.env['village_master.village_master'].search([]),
#         })

#     @http.route('/village_master/village_master/objects/<model("village_master.village_master"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('village_master.object', {
#             'object': obj
#         })
