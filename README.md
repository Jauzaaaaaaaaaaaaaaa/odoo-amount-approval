# Odoo 17 Amount Approval

Two small Odoo 17 modules that add an amount-based approval step to Sales and Purchase.
An order whose total is above a limit set in Settings waits in **Waiting Approval** until a user in
the **Amount Approver** group approves it, or rejects it with a reason logged in the chatter.

| Module | App | Details |
|--------|-----|---------|
| [`sale_amount_approval`](sale_amount_approval) | Sales | Quotations above the limit wait before they become Sales Orders. |
| [`purchase_amount_approval`](purchase_amount_approval) | Purchase | RFQs above the limit wait before they become Purchase Orders. |

Each module works on its own: install only the one you need.

I wrote these as learning and portfolio projects after a 5-month Odoo internship.
I ran them on a local Odoo 17 and can explain how each part works (see each module's README).

## Install

1. Add this repository folder to your `addons_path`.
2. Restart Odoo, update the Apps list, and install **Sale Amount Approval** and/or **Purchase Amount Approval**.

Run all tests:

```
python odoo-bin -c odoo.conf -d <test_db> -i sale_amount_approval,purchase_amount_approval --test-enable --test-tags=/sale_amount_approval,/purchase_amount_approval --stop-after-init
```

## License

LGPL-3
