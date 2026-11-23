{
    'name': 'Sale Amount Approval',
    'version': '17.0.1.0.0',
    'summary': 'Sales orders above a set amount must be approved before they are confirmed',
    # Odoo would otherwise render README.md as reStructuredText and log warnings
    'description': 'Quotations above a limit set in Settings wait in "Waiting Approval" '
                   'until a Sales Amount Approver approves or rejects them. See README.md.',
    'category': 'Sales/Sales',
    'author': 'Jauza Fawaid',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/sale_amount_reject_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
}
