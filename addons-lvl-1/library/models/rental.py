from odoo import models, fields

class Rental(models.Model):
    _name = 'library.rental'
    _description = 'Book Rental'

    rental_date = fields.Date(string='Rental Date', required = True)
    return_date = fields.Date(string='Return Date')

    book_id = fields.Many2one('library.book', string='Book')
    customer_id = fields.Many2one('library.partner', string="Customer")
    