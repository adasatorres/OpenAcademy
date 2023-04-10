from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
class Lead(models.Model):
    _inherit = 'crm.lead'

    def send_email(self):
        ids = self.env.ref('crm_open_academy.confirmacion_template_email').id
        template = self.env['mail.template'].browse(ids)
        template.send_mail(self.id,force_send=True)
    
    
    @api.model
    def create(self, args):
        lead = super(Lead, self).create(args)
        if int(args['medium_id']) == 1:
            lead.send_email()
        return lead