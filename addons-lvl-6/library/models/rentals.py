# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'
    _order = "rental_date desc,return_date desc"

    customer_id = fields.Many2one(
        'res.partner',
        'Customer',
        domain=[('customer', '=', True), ],
        required=True,
    )
    book_id = fields.Many2one(
        'product.product',
        'Book',
        domain=[('book', '=', True)],
        required=True,
    )
    rental_date = fields.Date(
        string='Rental date', required=True, default=lambda self: fields.Date.today())
    return_date = fields.Date(string='Return date', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('rented', 'Rented'),
        ('returned', 'Returned'),
        ('lost', 'Lost')
    ], default='draft', string='State')

    @api.multi
    def action_mark_as_rented(self):
        for r in self:
            r.state = 'rented'
            r.book_id.state = 'rented'
            r.compute_rent_price()

    @api.multi
    def action_mark_as_return(self):
        for r in self:
            r.state = 'returned'
            r.book_id.state = 'available'

    @api.multi
    def action_mark_as_lost(self):
        for r in self:
            r.state = 'lost'
            r.book_id.state = 'lost'
            r.add_fine()

    @api.multi
    def compute_rent_price(self):
        for r in self:
            delta = fields.Date.from_string(
                r.return_date) - fields.Date.from_string(r.rental_date)
            pricing = self.env.ref('library.price_rent')
            amount = delta.days * pricing.price / pricing.duration
            r.add_payment(r.customer_id, amount)

    @api.multi
    def add_fine(self):
        for r in self:
            pricing = self.env.ref('library.price_loss')
            r.add_payment(r.customer_id, pricing.price)

    def add_payment(self, customer_id, amount):
        print('customer_id', customer_id)
        self.env['library.payment'].create({
            'amount': amount,
            'customer_id': customer_id.id
        })
    
    @api.model
    def _cron_check_date(self):
        late_rentals = self.search([('state','=','rented'), ('return_date', '<', fields.Date.today() )])
        template_id = self.env.ref('library.mail_template_book_return')
        for rec in late_rentals:
            mail_id = template_id.send_mail(rec.i)


class Pricing(models.Model):
    _name = 'library.pricing'

    name = fields.Char('Name')
    price = fields.Float('Price')
    duration = fields.Integer('Duration in Days')
    pricing_type = fields.Selection([
        ('linear', 'Linear'),
        ('fixed', 'Fixed')
    ], string='Pricing Type')


class Payment(models.Model):
    _name = 'library.payment'

    amount = fields.Float('Amount', required=True)
    customer_id = fields.Many2one('res.partner', 'Customer', domain=[
                                  ('customer', '=', True)])
