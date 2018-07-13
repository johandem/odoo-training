from odoo import models, fields


class Session(models.Model):
    _name = 'citadel.session'
    start_date = fields.Date('Start Date')
    duration = fields.Integer('Duration in Days')
    course_id = fields.Many2one(
        'citadel.course', string="Course", required=True, ondelete='cascade')
    instructor_id = fields.Many2one('citadel.partner', string="Instructor")
    attendee_ids = fields.Many2many('citadel.partner', string="Attendees")
    status = fields.Selection([
        ('in_preparation', 'In Preparation'),
        ('given', 'Given')
    ])
    active = fields.Boolean('Active?', default=1)
