{
    'name': 'Mass Payments',
    'version': '0.0.1',
    'Author': 'AAAAAAAA',
    'category': 'Accounting',
    'summary': 'Manage Mass Payments',
    'description': """
        This module allows you to manage mass payments to multiple invoices.
    """,
    'depends': ['account'],
    'data': [
        'views/mass_payment_views.xml',
        'views/mass_payment_wizard_views.xml',
    ],
    'installable': True,
}