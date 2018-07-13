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

class RentalWizard(models.TransientModel):
    _name = 'library.rental.wizard'

    book_ids = fields.Many2many('product.product', domain="[('book', '=', 1)]")

class PartnerWizard(models.TransientModel):
    _name = 'library.partner.wizard'

    partner_ids = fields.Many2many('res.partner')