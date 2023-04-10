from odoo import models, fields, api
from odoo.exceptions import ValidationError


class sesiones(models.Model):
    _name = "openacademy.sesiones"
    _inherit = ['portal.mixin','mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']
    _description = "Modelo de las sesiones"
    _rec_name = "nombre"

    nombre = fields.Char(string="Nombre" , required=True)
    fecha_inicio = fields.Date(string="Fecha inicio", default = fields.Date().context_today)
    fecha_fin = fields.Date(string="Fecha fin")
    duracion = fields.Float(string="Duración")
    numero_asientos = fields.Integer(string= "Número de asientos",on_change='_validar_asientos')
    instructor_id = fields.Many2one(string="Instructor", comodel_name="res.partner", domain="['|',('instructor','=','true'),('category_id','like','Profesor/')]")
    curso_id = fields.Many2one(string="Curso", comodel_name="openacademy.cursos", required=True)
    asistentes_ids = fields.Many2many(string="Asistentes", comodel_name="res.partner")
    num_asistentes = fields.Integer(string="Número de asistentes",default=0, compute="_count_asistentes", store=True)
    num_asientos_ocupado = fields.Integer(string="Numero de asientos ocupados", on_change='_validar_asientos_ocupados')
    num_asientos_ocupado_porcentaje = fields.Float(string="Asientos ocupados en %", compute="_num_asientos_porcen")
    descripcion_sesion = fields.Html(string="Descripcion de la sesión")
    activa = fields.Boolean(string="Activo", default=1)
    
    
    # método que calcula el porcentaje de asientos ocupados.
    @api.depends('num_asientos_ocupado')
    def _num_asientos_porcen(self):
        for record in self:
            if record.numero_asientos != 0:
                record.num_asientos_ocupado_porcentaje = 100 * record.num_asientos_ocupado / record.numero_asientos
            else:
                record.num_asientos_ocupado_porcentaje = 0

    @api.depends('asistentes_ids')
    def _count_asistentes(self):
        for record in self:
            record.num_asistentes = len(record.asistentes_ids)


    # método que comprueba el número de asientos no sea negativo y manda una advertencia.
    @api.onchange('numero_asientos')
    def _validar_asientos(self):
        if self.numero_asientos < 0:
            return {
        'warning': {
            'title': "Advertencia",
            'message': "El valor de numero de los asientos no puede ser menor de 0."
        }
            }
    # método que comprueba el número de asientos ocupado no sea negativo y no sea superior al numero de asientos y manda una advertencia.
    @api.onchange('num_asientos_ocupado')
    def _validar_asientos_ocupados(self):
        if self.num_asientos_ocupado  < 0 or self.num_asientos_ocupado > self.numero_asientos:
             return {
        'warning': {
            'title': "Advertencia",
            'message': "El valor de numero de los asientos ocupados no puede ser menor de 0 o mayor del numero de asientos."
        }
            }

    # método que valida si el asistente que vas a añadir no es el instructor.
    @api.constrains('asistentes_ids','instructor_id')
    def _validar_instructor_en_asistentes(self):
        for record in self:
            ids = record.asistentes_ids.ids 
            if record.instructor_id.id in ids and record.instructor_id != None: 
                raise ValidationError("El instructor se encuentra entre los asistentes")
    
    # método que valida si la fecha de fin es mayor que la fecha de inicio.
    @api.constrains('fecha_fin')
    def _validar_fecha_fin(self):
        for record in self:
            if record.fecha_fin <= record.fecha_inicio:
                raise ValidationError("La fecha de fin no puede ser menor o igual a la fecha de inicio")
            
            


