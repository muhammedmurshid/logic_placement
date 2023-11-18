{
    'name': "Placements",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base','mail', 'logic_base'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/placements.xml',
        # 'views/account_payment_views.xml',
        # 'wizard/register_pay_wizard_views.xml',
        # 'data/activity.xml',
    ],
    'demo': [],
    'summary': "placements",
    'description': "Logic Placements",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}