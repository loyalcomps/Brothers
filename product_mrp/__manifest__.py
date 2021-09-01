# -*- coding: utf-8 -*-
{
    'name': "product_mrp",

    'summary': """
       product mrp""",

    'description': """
       product mrp
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','stock','stock_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/templates.xml',
        'views/stock.xml',
        'views/views.xml',
        'views/sale.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
