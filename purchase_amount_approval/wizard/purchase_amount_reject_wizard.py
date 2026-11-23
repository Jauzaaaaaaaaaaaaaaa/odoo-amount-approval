from odoo import _, fields, models


class PurchaseAmountRejectWizard(models.TransientModel):
    _name = 'purchase.amount.reject.wizard'
    _description = 'Reject Purchase Order'

    order_id = fields.Many2one('purchase.order', required=True)
    reason = fields.Text(required=True)

    def action_reject(self):
        self.ensure_one()
        order = self.order_id
        order._check_amount_approver()
        order.state = 'draft'
        order.message_post(body=_("Rejected by %(user)s. Reason: %(reason)s",
                                  user=self.env.user.name, reason=self.reason))
