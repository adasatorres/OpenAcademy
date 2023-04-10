from odoo import models, fields, api
from lxml import etree


class asistentes(models.TransientModel):
    _name = "openacademy.asistentes"

    def _default(self):
        return self.env["openacademy.sesiones"].browse(self._context.get("active_ids"))


    sesiones_ids = fields.Many2many(string="Sesiones", comodel_name="openacademy.sesiones", default=_default)
    asistentes_ids = fields.Many2many(comodel_name="res.partner", string="Asistentes")

    def ok(self):
        for sesion in self.sesiones_ids:
            sesion.asistentes_ids |= self.asistentes_ids
        return {}

    def cancel(self):
        pass
