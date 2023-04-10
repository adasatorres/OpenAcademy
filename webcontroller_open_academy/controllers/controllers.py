# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


# class WebcontrollerOpenAcademy(http.Controller):
#     @http.route('/webcontroller_open_academy/webcontroller_open_academy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/webcontroller_open_academy/webcontroller_open_academy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('webcontroller_open_academy.listing', {
#             'root': '/webcontroller_open_academy/webcontroller_open_academy',
#             'objects': http.request.env['webcontroller_open_academy.webcontroller_open_academy'].search([]),
#         })

#     @http.route('/webcontroller_open_academy/webcontroller_open_academy/objects/<model("webcontroller_open_academy.webcontroller_open_academy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('webcontroller_open_academy.object', {
#             'object': obj
#         })

