from odoo import http
from odoo.http import request


class Main(http.Controller):
    @http.route('/library/books', type='http', auth='public', website=True)
    def books(self):
        records = request.env['product.product'].search([])
        return request.render('library.book_rent', {
            'books': records
        })
    
    @http.route('/library/books/json', type='json', auth='none')
    def books_json(self):
        records = request.env['product.product'].sudo().search([])
        return records.read(['name'])
