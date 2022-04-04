# -*- coding: utf-8 -*-
from odoo import http

# class Sua(http.Controller):
#     @http.route('/sua/sua/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sua/sua/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sua.listing', {
#             'root': '/sua/sua',
#             'objects': http.request.env['sua.sua'].search([]),
#         })

#     @http.route('/sua/sua/objects/<model("sua.sua"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sua.object', {
#             'object': obj
#         })