# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Partner(models.Model):
    _inherit = 'res.partner'

    author = fields.Boolean('is an Author', default=False)
    publisher = fields.Boolean('is a Publisher', default=False)

    current_rental_ids = fields.One2many(
            'library.rental',
            'customer_id',
            string='Rentals', domain=[('state', '=', 'rented'), ])
    old_rental_ids = fields.One2many(
        'library.rental',
        'customer_id',
        string='Rentals', domain=[('state', '=', 'returned'), ])
    lost_rental_ids = fields.One2many(
        'library.rental',
        'customer_id',
        string='Rentals', domain=[('state', '=', 'lost'), ])

    book_ids = fields.Many2many(
        comodel_name="product.product",
        string="Books",
        domain=[('book', '=', True), ],
    )
    nationality_id = fields.Many2one(
        'res.country',
        'Nationality',
    )
    birthdate = fields.Date('Birthdate',)

    payment_ids = fields.One2many(
        'library.payment', 'customer_id', readonly=True, string='Payments')
    amount_owed = fields.Float(
        compute='_compute_amount_owed', store=True, string='Amount Owed')

    @api.multi
    @api.depends('payment_ids')
    def _compute_amount_owed(self):
        for r in self:
            r.amount_owed = sum(r.payment_ids.mapped('amount'))
