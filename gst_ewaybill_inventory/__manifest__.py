# -*- coding: utf-8 -*-
{
    'name': "GST Ewaybill Inventory",

    'summary': """
        Module helps to create GST Eway Bill for Internal Transfer""",

    'description': """
        Module helps to create GST Eway Bill for Internal Transfer
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'gst_ewaybill'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/ewaybill_server_actions.xml',
        'views/consolidated_ewaybill_view.xml',
        'views/studio_inventory_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
