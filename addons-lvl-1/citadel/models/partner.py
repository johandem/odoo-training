from odoo import models, fields


class Partner(models.Model):
    _name = 'citadel.partner'
    name = fields.Char('Name', required=True)
    is_instructor = fields.Boolean('Instructor?')
    session_ids = fields.Many2many(
        'citadel.session', string='Attended Sessions', readonly=True)
    # course_ids = fields.One2many(
    #     'citadel.course', string='Supervised Courses', readonly=True)
    # session_ids = fields.One2many(
    #     'citadel.session', string='Given Sessions', readonly=True)
