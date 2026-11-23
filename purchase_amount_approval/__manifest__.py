{
    'name': 'Purchase Amount Approval',
    'version': '17.0.1.0.0',
    'summary': 'Purchase orders above a set amount must be approved before they are confirmed',
    # Odoo would otherwise render README.md as reStructuredText and log warnings
    'description': 'Purchase orders above a limit set in Settings wait in "Waiting Approval" '
                   'until an Amount Approver approves or rejects them. See README.md.',
    'category': 'Inventory/Purchase',
    'author': 'Jauza Fawaid',
    'license': 'LGPL-3',
    'depends': ['purchase'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/purchase_amount_reject_wizard_views.xml',
        'views/purchase_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
}
