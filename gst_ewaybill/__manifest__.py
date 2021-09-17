# -*- coding: utf-8 -*-
{
    'name': "GST Ewaybill",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'uom', 'sale_stock', 'mail', 'wk_wizard_messages'],

    # always loaded
    'data': [
        'security/ewaybill_security.xml',
        'security/ir.model.access.csv',
        'data/data_unit_quantity.xml',
        'data/ewaybill_server_actions.xml',
        'wizard/consolidated_ewaybill_view.xml',
        'wizard/vehicle_no_updation_view.xml',
        'views/ewaybill_uqc_view.xml',
        'views/ewaybill_transporter_form_view.xml',
        'views/ewaybill_transporter_tree_view.xml',
        'views/gst_ewaybill_action_view.xml',
        'views/gst_ewaybill_menu_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
