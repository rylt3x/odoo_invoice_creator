# -*- coding: utf-8 -*-
{
    'name': "Invoice Creator",
    'summary': """Invoice create software""",
    'description': """Create invoice by loading file""",

    'author': "Mikhail",
    'website': "https://github.com/rylt3x",
    'category': 'Productivity',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
}
