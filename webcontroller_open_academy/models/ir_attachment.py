from odoo import models, fields, api

class irAttachmentWebController(models.Model):
   _inherit = "ir.attachment"
   sesiones_id = fields.Many2one(comodel_name="openacademy.sesiones", string="Sesion")