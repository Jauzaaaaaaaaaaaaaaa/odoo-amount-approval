from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    so_amount_approval_limit = fields.Monetary(
        string='Sales Approval Limit',
        currency_field='currency_id',
        help='Quotations with a total above this amount (in company currency) '
             'must be approved by a Sales Amount Approver. 0 turns the check off.',
    )
