# -*- coding: utf-8 -*-
{
    'name': "brothers_invoice_print",

    'summary': """
       Invoice print""",

    'description': """
        Invoice print
    """,

    'author': "Loyal It Solutions PVT LTD",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','free_qty','report_qweb_pdf_watermark','customer_product_qrcode'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/invoice_menu.xml',
        'views/invoices_temp.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
