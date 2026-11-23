from odoo import _, fields, models
from odoo.exceptions import AccessError

APPROVER_GROUP = 'purchase_amount_approval.group_po_amount_approver'


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # ('sent',) is a reference point: the new state is placed right after "RFQ Sent"
    state = fields.Selection(
        selection_add=[('sent',), ('to_approve', 'Waiting Approval')],
        ondelete={'to_approve': 'set default'},
    )

    def _needs_amount_approval(self):
        self.ensure_one()
        limit = self.company_id.po_amount_approval_limit
        if not limit or self.env.user.has_group(APPROVER_GROUP):
            return False
        total = self.currency_id._convert(
            self.amount_total, self.company_id.currency_id, self.company_id,
            self.date_order or fields.Date.today())
        return total > limit

    def _check_amount_approver(self):
        # Buttons hidden with groups="" are only a UI hint; this is the real check.
        if not self.env.user.has_group(APPROVER_GROUP):
            raise AccessError(_("Only Purchase Amount Approvers can approve or reject this order."))

    def button_confirm(self):
        waiting = self.filtered(lambda o: o.state in ('draft', 'sent') and o._needs_amount_approval())
        for order in waiting:
            order.state = 'to_approve'
            order.message_post(body=_("The order total is above the approval limit. Waiting for approval."))
        return super(PurchaseOrder, self - waiting).button_confirm()

    def action_amount_approve(self):
        self._check_amount_approver()
        orders = self.filtered(lambda o: o.state == 'to_approve')
        # Back to draft so the standard confirm flow runs (vendor prices, receipts, ...).
        orders.state = 'draft'
        for order in orders:
            order.message_post(body=_("Approved by %s.", self.env.user.name))
        return orders.button_confirm()
