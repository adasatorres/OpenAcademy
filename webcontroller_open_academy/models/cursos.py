from odoo import models, fields, api


class cursosInherit(models.Model):
    _inherit = ['openacademy.cursos']
    galeria_ids = fields.Many2many(comodel_name="web_controller_open_academy.galeria", string="Galeria de Imagenes")