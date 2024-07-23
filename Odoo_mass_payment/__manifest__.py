{
    'name': 'Mass Payments',
    'version': '0.0.1',
    "author": "AAAAAAAA",
    "license": "AGPL-3",
    'installable': True,
    'category': 'Payment',
    'summary': 'Manage Mass Payments',
    'description': """
        This module allows you to manage mass payments to multiple invoices.
    """,
    'depends': ['account_payment'],
    'data': [
        'views/mass_payment_views.xml',
        'views/mass_payment_wizard_views.xml',
    ],
}