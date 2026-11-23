from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # related + readonly=False: the Settings page reads and writes the company field directly
    so_amount_approval_limit = fields.Monetary(
        related='company_id.so_amount_approval_limit',
        currency_field='company_currency_id',
        readonly=False,
    )
