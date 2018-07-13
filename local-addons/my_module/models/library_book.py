from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.fields import Date as fDate
from datetime import timedelta


class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive']
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    short_name = fields.Char(
        string='Short Title',
        required=True,
        size=100,
        translate=False,)
    notes = fields.Text('Internal Notes')
    state = fields.Selection([('draft', 'Not Available'),
                              ('available', 'Available'),
                              ('borrowed', 'Borrowed')
                              ('lost', 'Lost')],
                             'State')
    description = fields.Html(
        string='Description',
        sanitize=True,
        strip_style=False,
        translate=False,)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'lost': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,)
    reader_rating = fields.Float('Reader Average Rating', digits=(14, 4),)
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))

    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price', currency_field='currency_id',)

    author_ids = fields.Many2many('res.partner', string='Authors')

    publisher_id = fields.Many2one(
        'res.partner', string='Publisher', ondelete='set null', context={}, domain=[])
    publisher_city = fields.Char(
        'Publisher CIty', related='publisher_id.city', readonly=True)

    # computed fields
    age_days = fields.Float(string='Days since Release', compute='_compute_age',
                            inverse='_inverse_age', search='_search_age', store=False, compute_sudo=False)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be unique.')
    ]

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 "%s (%s)" % (record.name, record.date_release)
                 ))
        return result

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if (record.date_release and record.date_release > fields.Date.today()):
                raise models.ValidationError(
                    'Release date must be in the past')

    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (today - fDate.from_string(book.date_release))
            book.age_days = delta.days

    def _inverse_age(self):
        today = fDate.from_string(fDate.context_today(self))
        for book in self.filtered('release_date'):
            d = today - timedelta(days=book.age_days)
            book.date_release = fDate.to_string(d)

    def _search_age(self, operator, value):
        today = fDate.from_string(fDate.context_today(self))
        value_days = timedelta(days=value)
        value_date = fDate.to_string(today - value_days)
        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>='
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue

    @api.model
    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])

class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
        'library.book', 'publisher_id', string='Published Books')
    authored_book_ids = fields.Many2many(
        'library.book', string='Authored Books', relation='library_book_res_partner_rel')

    count_books = fields.Integer(
        'Number of Authored Books', compute='_compute_count_books')
    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    date = fields.Date('Date')
    is_company = fields.Boolean('Is a company', help="Check if the contact is a company, " "otherwise it is a person")
    parent_id = fields.Many2one('res.partner', 'Related Company')
    child_ids = fields.One2many('res.partner', 'parent_id', 'Contacts')
    
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for r in self:
            r.active = not r.active


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner', ondelete='cascade')

    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
