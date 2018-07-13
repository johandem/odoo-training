# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Courses(models.Model):
    _name = 'openacademy.course'

    name = fields.Char()
    user_id = fields.Many2one('res.users', string="Responsible")


class Sessions(models.Model):
    _name = 'openacademy.session'

    course_id = fields.Many2one('openacademy.course', string="Course")
    user_id = fields.Many2one('res.users', string="Instructor")
    start_date = fields.Date()
    seats = fields.Integer('Room Capacity')
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    seats_taken = fields.Integer('Seats Taken', compute='_compute_seats_taken', store=True)

    # client validation, on value change
    @api.onchange('seats', 'attendee_ids')
    def check_seats_taken(self):
        for r in self:
            if self.seats_taken > self.seats:
                return { 'warning': {
                    'title': 'Too many attendees',
                    'message': 'The room has %s seats and there are %s attendees registered.' % (r.seats, r.seats_taken)
                }}

    # python constaint, on controller, gives UI feedback
    @api.constrains('seats', 'attendee_ids')
    def _check_seats_limit(self):
        for r in self:
            if r.seats_taken > r.seats:
                raise ValidationError("Too many attendees: %s" % r.seats_taken)
    
    # computed field to update the UI and maybe store in db
    @api.depends('seats', 'attendee_ids')
    def _compute_seats_taken(self):
        for r in self:
            r.seats_taken = len(r.attendee_ids)

    # sql contraint
    _sql_constraints = [
        ('seats_taken_check',
        'CHECK(seats >= seats_taken)',
        'Room is full. Increase seats or remove excess attendees')    
    ]
