from odoo import models, fields


class Volunteer(models.Model):
    _name = 'coopplanning.volunteer'

    name = fields.Char('Name')

    work_type = fields.Selection([
        ('recurring', 'Recurring Tasks'),
        ('single', 'Single Task')
    ], string='Responsibilities')
