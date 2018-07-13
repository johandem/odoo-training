from odoo import models, fields


class Course(models.Model):
    _name = 'citadel.course'
    title = fields.Char('Title', required=True)
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ])

    responsible_id = fields.Many2one(
        'citadel.partner', string='Responsible')
    session_ids = fields.One2many(
        'citadel.session', 'course_id', string='Sessions', readonly=True)
