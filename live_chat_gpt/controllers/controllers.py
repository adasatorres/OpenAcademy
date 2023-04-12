# -*- coding: utf-8 -*-
# from odoo import http


# class LiveChatGpt(http.Controller):
#     @http.route('/live_chat_gpt/live_chat_gpt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/live_chat_gpt/live_chat_gpt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('live_chat_gpt.listing', {
#             'root': '/live_chat_gpt/live_chat_gpt',
#             'objects': http.request.env['live_chat_gpt.live_chat_gpt'].search([]),
#         })

#     @http.route('/live_chat_gpt/live_chat_gpt/objects/<model("live_chat_gpt.live_chat_gpt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('live_chat_gpt.object', {
#             'object': obj
#         })
