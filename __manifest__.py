# -*- coding: utf-8 -*-
{
    'name': "SUA (Sistema Único de Autodeterminación)",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "José Roberto Mejía Pacheco",
    'website': "https://www.facebook.com/isscjrmp",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sua_aseg.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}