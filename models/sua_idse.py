from odoo import _, api, fields, models
CLAVE_DE_UBICACION = '                 '
CREDITO_INFONAVIT = False
LONG10 = 10
LONG17 = 17
LONG1 = 1
LONG2 = 2
LONG3 = 3
LONG4 = 4
LONG5 = 5
LONG6 = 6
LONG13 = 13
LONG18 = 18
LONG50 = 50
LONG25 = 25
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
    'clave_de_ubicacion','clave_de_municipio','clave_lugar_de_nacimiento','sexo']
FIELDS_TO_STRIP=['registro_patronal_imss','reg_fed_de_contribuyentes','curp',
    'nombre','apellido_paterno','apellido_materno','clave_de_municipio','ocupacion','clave_lugar_de_nacimiento','sexo']
DEFAULT_NUMERO_CREDITO_INFONAVIT='          '

class Idse(models.Model):
    _name = 'sua.idse'
    _description = ' IMSS Desde Su Empresa'

    registro_patronal_imss = fields.Char(string='Registro Patronal',size=LONG11)
    digito_verificador_registro_patronal = fields.Char(compute='_compute_digito_verificador_de_registro_patronal',string='Dígito Verificador Registro Patronal',size=LONG1)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social',size=LONG11)
    digito_verificador_numero_de_seguridad_social = fields.Char(compute='_compute_digito_verificador_de_seguridad_social',string='Dígito Verificador Número de Seguridad Social')
    apellido_paterno = fields.Char(string='Apellido Paterno')
    apellido_materno = fields.Char(string='Apellido Materno')
    nombre = fields.Char(string='Nombre(s) Separados por Espacio',help='Ejemplo Kaleth Chalino Valentin')
    nombre_apellidopaterno_materno_nombre = fields.Char(compute='_compute_nombre_apellidopaterno_materno_nombre', string='Nombre Completo Formato SUA')
    salario_base_cotizacion = fields.Char(string='Salario Base Cotización')
    filler1 = fields.Char(string='Filler',default='      ')
    tipo_de_trabajador = fields.Selection(
        string='Tipo de Trabajador',
        selection=[('1', 'Trab. permanente'), ('2', ' Trab. Ev. Ciudad'),('3', 'Trab. Ev. Construcción'),('4', 'Eventual del campo')]
    )
    tipo_de_salario = fields.Selection(string='Tipo de Salario', selection=[('0', 'Fijo'), ('1', 'Variable'),('2', 'Mixto')])
    jornada_semana_reducida = fields.Selection(
        string='Jornada/Semana Reducida',
        selection=[('1', 'Un día'), ('2', 'Dos dias'),('3', 'Trab. Ev. Construcción'),('4', 'Cuatros días'),
        ('5', 'Cinco días'),('6', 'Seis días'),('0', 'Jornada Normal')]
    )
    fecha_de_movimiento = fields.Char(string='Fecha del Movimiento',required=True,size=LONG8)
    unidad_de_medicina_familiar = fields.Char(string='Unidad de Medicina Familiar')
    filler2 = fields.Char(string='Filler',default='  ')
    tipo_de_movimiento = fields.Selection(string='Tipo de Movimiento',required=True, selection=[('02', 'Baja'), ('07', 'Modificación de Salario'),
    ('08', 'Reingreso'),('09', 'Aportación Voluntaria'),('11', 'Ausentismo'),('12', 'Incapacidad')])
    guia = fields.Char(string='Guia')
    clave_de_trabajador = fields.Char(string='Clave del Trabajador')
    filler3 = fields.Char(string='Filler',default=' ')
    curp = fields.Char(string='CURP')
    identificador_del_formato = fields.Char(string='Identificador del Formato',default=9)
    
