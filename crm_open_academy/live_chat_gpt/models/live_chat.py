from odoo import models, fields, api

class LiveChat(models.Model):
    _inherit = 'im_livechat.channel'

    @api.model
    def _get_available_users(self):
        """ get available user of a given channel
            :retuns : return the res.users having their im_status online
        """
        self.ensure_one()
        return self.user_ids.filtered(lambda user: user.im_status == 'online' or user.name.lower() == 'chatgpt')