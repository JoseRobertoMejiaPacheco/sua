from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    registro_patronal = fields.Char(string='Registro Patronal',help="Registro Patronal requiere 11 Carácteres Alafanuméricos")
    
