from odoo import models, fields


class LibraryPartner(models.Model):
    _name = 'library.partner'

    name = fields.Char('Name')
    address = fields.Text('Address')  # fields.Text because multiline
    email = fields.Char('email')
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('author', 'Author')
    ], default='customer')
    rental_ids = fields.One2many(
        comodel_name='library.rental',
        inverse_name='customer_id',
        string='Rentals'
    )
