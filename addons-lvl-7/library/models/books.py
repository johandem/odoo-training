# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Books(models.Model):
    _inherit = 'product.product'

    author_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Authors",
        domain=[('author','=',True), ],
    )
    edition_date = fields.Date(string='Edition date',)
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one(
        'res.partner',
        string='Publisher',
        domain=[('publisher','=',True), ],
    )
    rental_ids = fields.One2many(
        'library.rental',
        'book_id',
        string='Rentals',)
    book = fields.Boolean('is a book', default=False)

    customer_count = fields.Integer('Customer Count', compute="_compute_customer_count")

    @api.depends('rental_ids.customer_id')
    def _compute_customer_count(self):
        for r in self:
            r.customer_count = len(r.mapped('rental_ids.customer_id'))

    @api.multi
    def open_customers(self):
        self.ensure_one()
        customer_ids = self.rental_ids.mapped('customer_id')
        return {
            'name': 'Customers of %s' % (self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', customer_ids.ids)],
        }