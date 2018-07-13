from odoo import models, fields


class Book(models.Model):
    _name = 'library.book'

    title = fields.Char('Title', required=True)
    edition_date = fields.Date('Year of Edition')
    isbn = fields.Char('ISBN', required=True)

    author_ids = fields.Many2many('library.partner', string='Authors')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    rental_ids = fields.One2many(
        comodel_name='library.rental',
        inverse_name='book_id',
        string='Rentals'
    )