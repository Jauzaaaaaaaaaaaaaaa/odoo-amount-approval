from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged('post_install', '-at_install')
class TestPurchaseAmountApproval(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.po_amount_approval_limit = 1000
        cls.env.company.po_double_validation = 'one_step'  # keep Odoo's own approval out of the way
        cls.buyer = new_test_user(cls.env, login='pa_buyer', groups='purchase.group_purchase_user')
        cls.approver = new_test_user(
            cls.env, login='pa_approver', groups='purchase_amount_approval.group_po_amount_approver')
        cls.vendor = cls.env['res.partner'].create({'name': 'Test Vendor'})
        cls.product = cls.env['product.product'].create({'name': 'Test Item'})

    def _new_order(self, price):
        return self.env['purchase.order'].with_user(self.buyer).create({
            'partner_id': self.vendor.id,
            'order_line': [Command.create({
                'product_id': self.product.id,
                'product_qty': 1,
                'price_unit': price,
                'taxes_id': [],
            })],
        })

    def test_small_order_is_confirmed_directly(self):
        order = self._new_order(500)
        order.button_confirm()
        self.assertEqual(order.state, 'purchase')

    def test_big_order_needs_approval(self):
        order = self._new_order(5000)
        order.button_confirm()
        self.assertEqual(order.state, 'to_approve')

        with self.assertRaises(AccessError):
            order.action_amount_approve()  # the buyer cannot approve their own order

        order.with_user(self.approver).action_amount_approve()
        self.assertEqual(order.state, 'purchase')

    def test_reject_sends_order_back_to_draft(self):
        order = self._new_order(5000)
        order.button_confirm()

        wizard = self.env['purchase.amount.reject.wizard'].with_user(self.approver).create({
            'order_id': order.id,
            'reason': 'Price too high',
        })
        wizard.action_reject()

        self.assertEqual(order.state, 'draft')
        self.assertIn('Price too high', order.message_ids[0].body)
