from odoo import models, fields, api

class cursos(models.Model):
    _name = "openacademy.cursos"
    _description = "Modelo de los cursos"
    _sql_constraints = [
        ('titulo_descripcion', 'CHECK (titulo IS DISTINCT FROM descripcion)', 'El título y la descripción no deben ser iguales.'),
        ('titulo_unico', 'UNIQUE(titulo)', 'El título ya existe.'),               
                        ]
    _rec_name = "name"


    
    titulo = fields.Char(string="Titulo" , required=True)
    descripcion = fields.Html(string="Descripción")
    responsable_id = fields.Many2one(string="Responsable", comodel_name="res.users", required=True)
    sesiones_ids = fields.One2many(string="Sesiones", comodel_name="openacademy.sesiones", inverse_name="curso_id")
    name = fields.Char(string="Nombre", compute="_name_compute")
    icono = fields.Image(string="Icono")
    documento = fields.Many2many(comodel_name='ir.attachment')

    

    @api.depends('titulo', 'responsable_id')
    def _name_compute(self):
        for curso in self:
            curso.name = curso.titulo + " - " + curso.responsable_id.name

    def copy(self, default : dict = {}):
        default.update({'titulo': f'Copia de {self.titulo} '})
        return super(cursos, self).copy(default)