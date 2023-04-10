from odoo import models, fields, api

class sesionesWebController(models.Model):
   _inherit = ['openacademy.sesiones']
   attachment_ids = fields.One2many(comodel_name="ir.attachment", inverse_name="sesiones_id", string="Attachments")
   