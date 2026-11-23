# Sale Amount Approval (Odoo 17)

A small Odoo 17 module: a quotation whose total is above a set limit cannot be confirmed
straight away. It goes to a new status, **Waiting Approval**, and a user in the
**Amount Approver** group must press **Approve** or **Reject** (with a reason).

It follows the same design as `purchase_amount_approval` in this repository, applied to the Sales app.

## What it does

1. **Settings → Sales → Amount Approval Limit**: set a limit in company currency (0 = off).
2. A salesperson clicks **Confirm**. If the total is above the limit, the quotation goes to
   **Waiting Approval** instead of becoming a Sales Order. A note is posted in the chatter.
3. An Amount Approver opens the quotation and clicks:
   - **Approve**: the quotation is confirmed the normal Odoo way (becomes a Sales Order).
   - **Reject**: a pop-up asks for a reason; the quotation goes back to draft and the reason is posted in the chatter.
4. Quotations at or under the limit, and quotations confirmed by an approver, are confirmed directly.

Sales administrators are automatically Amount Approvers.

## Install

1. Put the `sale_amount_approval` folder in a folder on your `addons_path`.
2. Restart Odoo, update the Apps list, install **Sale Amount Approval**.
3. Set the limit in Settings, and give users the role in
   *Settings → Users → (user) → Sales: Amount Approver*.

Run the tests:

```
python odoo-bin -c odoo.conf -d <test_db> -i sale_amount_approval --test-tags=/sale_amount_approval --stop-after-init
```

## How it works (file by file)

| File | What it does |
|------|--------------|
| `__manifest__.py` | Module card: name, version, depends on `sale`, and the list of XML/CSV files to load (security first, because views use the group). |
| `models/res_company.py` | Adds the field `so_amount_approval_limit` to the company, so each company can have its own limit. |
| `models/res_config_settings.py` | Shows that company field on the Settings page (`related=` + `readonly=False`). |
| `models/sale_order.py` | The main logic. (1) Adds `to_approve` to the existing `state` field with `selection_add`. (2) `_needs_amount_approval()` converts the total to company currency and compares it with the limit. (3) Overrides `action_confirm()`: quotations that need approval move to `to_approve`; the rest go to the original Odoo method through `super()`. (4) `action_amount_approve()` checks the user's group, puts the quotation back to draft, and calls `action_confirm()` again, so Odoo's normal confirm steps (deliveries, locking) still run. |
| `wizard/sale_amount_reject_wizard.py` | A `TransientModel` for the Reject pop-up with a required reason; `action_reject()` checks the group, sets the quotation back to draft, and posts the reason in the chatter. |
| `security/security.xml` | Creates the **Amount Approver** group. It implies "User: All Documents", and Sales Administrator implies it. |
| `security/ir.model.access.csv` | Access rights for the wizard model: only Amount Approvers can use it. |
| `views/sale_order_views.xml` | Inherits the sales order form and adds **Approve** and **Reject**, visible only in `to_approve` and only to approvers. |
| `views/res_config_settings_views.xml` | Adds the limit field to the Sales settings page, in "Quotations & Orders". |
| `wizard/sale_amount_reject_wizard_views.xml` | The pop-up form for the reject reason, and the window action that opens it. |
| `tests/test_amount_approval.py` | `TransactionCase` tests: a small quotation is confirmed directly; a big one waits, the salesperson cannot approve it, an approver can; rejecting sends it back to draft with the reason in the chatter. |

The design choices are the same as in the purchase module: security is checked on the server
(`AccessError`), `super()` is always called for orders that do not need approval, and the total is
converted to company currency before comparing.

## License

LGPL-3
