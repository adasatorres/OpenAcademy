from odoo import models, fields, api

class socios(models.Model):
    _inherit = 'res.partner'
    instructor = fields.Boolean(string="Instructor")
    sesiones_ids = fields.Many2many(string="Sesiones", comodel_name="openacademy.sesiones")
    