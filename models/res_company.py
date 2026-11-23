from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    po_amount_approval_limit = fields.Monetary(
        string='Purchase Approval Limit',
        currency_field='currency_id',
        help='Purchase orders with a total above this amount (in company currency) '
             'must be approved by an Amount Approver. 0 turns the check off.',
    )
