from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

CLAVE_DE_UBICACION = '                 '
CREDITO_INFONAVIT = False
LONG10 = 10
LONG17 = 17
LONG1 = 1
LONG13 = 13
LONG18 = 18
LONG50 = 50
LONG7 = 7
LONG11 = 11

class SUAAseg(models.Model):
    _name = 'sua.aseg'
    _description = 'Formato del Archivo de Importación de Trabajadores ASEG.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal')
    numero_de_seguridad_social = fields.Integer(string='Número de Seguridad Social')
    reg_fed_de_contribuyentes = fields.Char(string='Registro Ferederal de Contribuyentes')
    curp = fields.Char(string='CURP')
    nombre = fields.Char(string='Nombre(s)')
    apellido_paterno = fields.Char(string='Apellido Paterno')
    apellido_materno = fields.Char(string='Apellido Materno')
    nombre_apellidopaterno_materno_nombre = fields.Char(compute='_compute_nombre_apellidopaterno_materno_nombre', string='Nombre')    
    @api.depends('nombre','apellido_paterno','apellido_materno')
    def _compute_nombre_apellidopaterno_materno_nombre(self):
        pass
    tipo_de_trabajador = fields.Integer(string='Tipo de Trabajador')
    jornada_semana_reducida = fields.Integer(string='Jornada/Semana Reducida')
    fecha_de_alta = fields.Integer(string='Fecha de Alta')
    salario_diario_integrado = fields.Integer(string='Salario Diario Integrado')
    clave_de_ubicacion = fields.Char(string='Clave De Ubicacion',default=CLAVE_DE_UBICACION)
    numero_de_credito_infonavit = fields.Char(string='Número De Crédito Infonavit')
    fecha_de_inicio_de_descuento = fields.Integer(string='Fecha de Inicio de Descuento')
    tipo_de_descuento = fields.Integer(string='Tipo de Descuento')
    valor_de_descuento = fields.Integer(string='Valor De Descuento')
    tipo_de_pension = fields.Integer(string='Tipo de Pension')
    clave_de_municipio = fields.Char(string='Clave De Municipio')


    @api.constrains('registro_patronal_imss','numero_de_seguridad_social')
    def _check_long_11(self):
        print(self)

    @api.constrains('reg_fed_de_contribuyentes')
    def _check_long_13(self):
        print(self)

    @api.constrains('curp')
    def _check_long_18(self):
        print(self)

    @api.constrains('nombre_apellidopaterno_materno_nombre')
    def _check_long_50(self):
        print(self)

    @api.constrains('fecha_de_alta','fecha_de_inicio_de_descuento','valor_de_descuento')
    def _check_long_8(self):
        print(self)

    @api.constrains('salario_diario_integrado')
    def _check_long_7(self):
        print(self)

    @api.constrains('clave_de_ubicacion')
    def _check_long_17(self):
        print(self)

    @api.constrains('numero_de_credito_infonavit')
    def _check_long_10(self):
        CREDITO_INFONAVIT = True if self.numero_de_credito_infonavit else  False
        self.__ev_long(self.numero_de_credito_infonavit,LONG10)



    @api.constrains('tipo_de_pension','tipo_de_trabajador','jornada_semana_reducida')
    def _check_long_1(self):
        print(self)

    def __ev_long(field_value,long,field_name="Test"):
        if CREDITO_INFONAVIT:
            if not len(field_value) == LONG10:
                raise ValidationError("El Campo ${field_name} debe contener ${LONG10} Carácteres")

