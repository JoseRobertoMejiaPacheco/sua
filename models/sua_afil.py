from odoo import _, api, fields, models
CLAVE_DE_UBICACION = '                 '
CREDITO_INFONAVIT = False
LONG10 = 10
LONG17 = 17
LONG1 = 1
LONG3 = 3
LONG4 = 4
LONG5 = 5
LONG6 = 6
LONG13 = 13
LONG18 = 18
LONG50 = 50
LONG7 = 7
LONG8 = 8
LONG11 = 11
LONG12 = 12
FILLZERO = "0"
FILLSPACE = " "
REPLACELEFT = 'left'
REPLACERIGHT = 'right'
NAME_SEPARATOR = '$'
FIELDS_TO_UPPER_CASE=[
    'registro_patronal_imss','reg_fed_de_contribuyentes','curp',
    'nombre','apellido_paterno','apellido_materno',
    'nombre_apellidopaterno_materno_nombre',
    'clave_de_ubicacion','clave_de_municipio']
FIELDS_TO_STRIP=['registro_patronal_imss','reg_fed_de_contribuyentes','curp',
    'nombre','apellido_paterno','apellido_materno','clave_de_municipio']
DEFAULT_NUMERO_CREDITO_INFONAVIT='          '



class SUAAfil(models.Model):
    _name = 'sua.afil'
    _description = 'Formato del Archivo de Importación de Trabajadores AFIL.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal',default= lambda self: self.env.user.company_id.registro_patronal,size=LONG10)
    digito_verificador_registro_patronal = fields.Char(string='Dígito Verificador Registro Patronal',size=LONG1)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social',size=LONG10)
    digito_verificador_numero_de_seguridad_social = fields.Char(string='Dígito Verificador Número de Seguridad Social')
    codigo_postal = fields.Char(string='Código Postal',size=LONG5)
    fecha_de_nacimiento = fields.Char(string='Fecha de Nacimiento',size=LONG8)
    lugar_de_nacimiento = fields.Selection(string='Lugar de Nacimiento', selection=[('key', 'value'), ('key', 'value')])
    unidad_de_medicina_familiar = fields.Char(string='Unidad de Medicina Familar',size=LONG3)
    ocupacion = fields.Char(string='Ocupación',size=LONG12)
    sexo = fields.Char(string='Sexo',size=LONG1)
    tipo_de_salario = fields.Selection(string='', selection=[('key', 'value'), ('key', 'value')])
    hora = fields.Char(string='Hora',size=LONG1)
