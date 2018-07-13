from odoo import models, fields


class Publisher(models.Model):
    _name = 'library.publisher'

    name = fields.Char('Name')
    