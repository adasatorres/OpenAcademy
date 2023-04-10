from odoo import models, fields, api

class GaleriaPhoto(models.Model):
    _name = 'web_controller_open_academy.galeria'
    _description = 'galeria de imagenes para cursos del modulo openacademy'
    _rec_name = 'nombre_photo'


    nombre_photo = fields.Char(string='Nombre de la imagen', required=True)
    data_photo = fields.Image(required=True)