# Purchase Amount Approval (Odoo 17)

A small Odoo 17 module: a purchase order whose total is above a set limit cannot be confirmed
straight away. It goes to a new status, **Waiting Approval**, and a user in the
**Amount Approver** group must press **Approve** or **Reject** (with a reason).

I wrote this as a learning and portfolio project after a 5-month Odoo internship.
I ran it on a local Odoo 17 and can explain how each part works (see "How it works" below).

## What it does

1. **Settings → Purchase → Amount Approval Limit**: set a limit in company currency (0 = off).
2. A buyer clicks **Confirm Order**. If the total is above the limit, the order goes to
   **Waiting Approval** instead of becoming a Purchase Order. A note is posted in the chatter.
3. An Amount Approver opens the order and clicks:
   - **Approve**: the order is confirmed the normal Odoo way (becomes a Purchase Order).
   - **Reject**: a pop-up asks for a reason; the order goes back to RFQ and the reason is posted in the chatter.
4. Orders at or under the limit, and orders confirmed by an approver, are confirmed directly.

Purchase administrators are automatically Amount Approvers.

## Relation to Odoo's built-in approval

Odoo already has *Settings → Purchase → Purchase Order Approval* (status "To Approve",
approved by Purchase Administrators). This module is a separate exercise that adds:

- its own approver group, so someone can approve orders without being a full Purchase Administrator;
- a **Reject** step with a required reason logged in the chatter.

Use one or the other. If both are on, an approved order may still stop at Odoo's own "To Approve" step.

## Install

1. Put the `purchase_amount_approval` folder in a folder on your `addons_path`.
2. Restart Odoo, update the Apps list, install **Purchase Amount Approval**.
3. Set the limit in Settings, and give users the role in
   *Settings → Users → (user) → Purchase: Amount Approver*.

Run the tests:

```
python odoo-bin -c odoo.conf -d <test_db> -i purchase_amount_approval --test-tags=/purchase_amount_approval --stop-after-init
```

## How it works (file by file)

| File | What it does |
|------|--------------|
| `__manifest__.py` | Module card: name, version, depends on `purchase`, and the list of XML/CSV files to load (security first, because views use the group). |
| `models/res_company.py` | Adds the field `po_amount_approval_limit` to the company, so each company can have its own limit. `Monetary` means it is shown with the company currency. |
| `models/res_config_settings.py` | Shows that company field on the Settings page. `related=` + `readonly=False` means the setting reads and writes the company field directly, no extra save code needed. |
| `models/purchase_order.py` | The main logic. (1) Adds the `to_approve` value to the existing `state` field with `selection_add`. (2) `_needs_amount_approval()` converts the order total to company currency and compares it with the limit. (3) Overrides `button_confirm()`: orders that need approval are moved to `to_approve`; all other orders go to the original Odoo method through `super()`. (4) `action_amount_approve()` checks the user's group, puts the order back to draft, and calls `button_confirm()` again, so Odoo's normal confirm steps still run. |
| `wizard/purchase_amount_reject_wizard.py` | A temporary model (`TransientModel`) for the Reject pop-up. It has the order and a required reason; `action_reject()` checks the group, sets the order back to draft, and posts the reason in the chatter. |
| `security/security.xml` | Creates the **Amount Approver** group. It implies Purchase User, and Purchase Administrator implies it, so the user form shows a simple dropdown: User / Amount Approver / Administrator. |
| `security/ir.model.access.csv` | Access rights for the new wizard model: only Amount Approvers can use it. Every new model in Odoo 17 needs a line here, or nobody can open it. |
| `views/purchase_order_views.xml` | Inherits the purchase order form and adds the **Approve** and **Reject** buttons, visible only in `to_approve` and only to approvers. |
| `views/res_config_settings_views.xml` | Inherits the Purchase settings page and adds the limit field under the built-in approval setting. |
| `wizard/purchase_amount_reject_wizard_views.xml` | The pop-up form for the reject reason, and the window action that opens it. |
| `tests/test_amount_approval.py` | Automated tests (`TransactionCase`, each test is rolled back): a small order is confirmed directly; a big order waits, a normal buyer cannot approve it, an approver can; rejecting sends it back to draft with the reason in the chatter. |

### Design choices worth knowing

- **Security is checked on the server**, not only by hiding buttons. `groups=` on a button only hides it;
  someone could still call the method through the API. That is why `_check_amount_approver()` raises
  an `AccessError`.
- **`super()` is always called** for orders that do not need approval, so other modules that also
  extend `button_confirm()` keep working.
- **Currency conversion**: the limit is in company currency, but an order can be in another currency,
  so the total is converted with `_convert()` before comparing.
- **Not done on purpose** (possible next steps): email or activity notification to approvers,
  multi-level approval, and a list/filter of orders waiting for approval.

## License

LGPL-3
