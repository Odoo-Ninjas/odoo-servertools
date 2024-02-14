from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Hook(models.Model):
    _name = "mousetrap.hook"
    _inherit = "method_hook.trigger.mixin"

    config_id = fields.Many2one("mousetrap.configuration")

    def _trigger(self, instances, args_packed, method):
        self.config_id._start_by_methodhook(instances, args_packed, method)
