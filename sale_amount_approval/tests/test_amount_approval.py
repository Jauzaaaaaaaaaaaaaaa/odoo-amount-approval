from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged('post_install', '-at_install')
class TestSaleAmountApproval(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.so_amount_approval_limit = 1000
        cls.salesperson = new_test_user(
            cls.env, login='sa_salesperson', groups='sales_team.group_sale_salesman')
        cls.approver = new_test_user(
            cls.env, login='sa_approver', groups='sale_amount_approval.group_so_amount_approver')
        cls.customer = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.product = cls.env['product.product'].create({'name': 'Test Item', 'type': 'service'})

    def _new_order(self, price):
        return self.env['sale.order'].with_user(self.salesperson).create({
            'partner_id': self.customer.id,
            'order_line': [Command.create({
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': price,
                'tax_id': [],
            })],
        })

    def test_small_order_is_confirmed_directly(self):
        order = self._new_order(500)
        order.action_confirm()
        self.assertEqual(order.state, 'sale')

    def test_big_order_needs_approval(self):
        order = self._new_order(5000)
        order.action_confirm()
        self.assertEqual(order.state, 'to_approve')

        with self.assertRaises(AccessError):
            order.action_amount_approve()  # the salesperson cannot approve their own quotation

        order.with_user(self.approver).action_amount_approve()
        self.assertEqual(order.state, 'sale')

    def test_reject_sends_order_back_to_draft(self):
        order = self._new_order(5000)
        order.action_confirm()

        wizard = self.env['sale.amount.reject.wizard'].with_user(self.approver).create({
            'order_id': order.id,
            'reason': 'Discount too high',
        })
        wizard.action_reject()

        self.assertEqual(order.state, 'draft')
        self.assertIn('Discount too high', order.message_ids[0].body)
