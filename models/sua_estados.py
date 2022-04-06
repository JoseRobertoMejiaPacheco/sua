from odoo import _, api, fields, models
class SUAEstados(models.Model):
    _name = 'sua.estados'
    _description = 'Datos de Estados Sua'
    cod_pos = fields.Char(string='Código Postal')
    descripcion = fields.Char(string='Descripción')
    cve_curp = fields.Char(string='Clave')
