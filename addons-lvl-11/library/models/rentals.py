# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'
    _order = "rental_date desc,return_date desc"

    customer_id = fields.Many2one(
        'res.partner',
        'Customer',
        domain=[('customer','=',True), ],
        required=True,
    )
    book_id = fields.Many2one(
        'product.product',
        'Book',
        domain=[('book','=',True)],
        required=True,
    )
    rental_date =  fields.Date(string='Rental date', required=True, default=lambda self: fields.Date.today())
    return_date =  fields.Date(string='Return date', required=True)

    @api.multi
    def rent_book(self, book_id, rental_date, return_date):
        rental = self.env['library.rental'].search([
            ('customer_id', '=', user_id)
            ], limit=1)
        if not rental:
            self.env['library.rental'].create({
                'customer_id': user_id,
                'book_id': book_id,
                'rental_date': rental_date,
                'return_date': return_date
            })

        
