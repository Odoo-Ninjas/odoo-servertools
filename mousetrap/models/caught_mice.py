from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Caught(models.Model):
    _name = "mousetrap.catches"
    _order = "id desc"

    excinfo = fields.Char("Exception")
    stacktrace = fields.Text("Stack Trace")
