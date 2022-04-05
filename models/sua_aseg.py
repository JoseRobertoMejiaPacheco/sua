from pickletools import long1
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
LONG8 = 8
LONG11 = 11
FILLZERO = "0"
FILLSPACE = " "
REPLACELEFT = 'left'
REPLACERIGHT = 'left'

# === Model sua.aseg for template of ASEG.txt===
class SUAAseg(models.Model):
    _name = 'sua.aseg'
    _description = 'Formato del Archivo de Importación de Trabajadores ASEG.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal',default= lambda self: self.env['res.company']._company_default_get().registro_patronal)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social')
    reg_fed_de_contribuyentes = fields.Char(string='Registro Ferederal de Contribuyentes')
    curp = fields.Char(string='CURP')
    nombre = fields.Char(string='Nombre(s)')
    apellido_paterno = fields.Char(string='Apellido Paterno')
    apellido_materno = fields.Char(string='Apellido Materno')
    nombre_apellidopaterno_materno_nombre = fields.Char(compute='_compute_nombre_apellidopaterno_materno_nombre', string='Nombre Completo Formato SUA')    
    tipo_de_trabajador = fields.Char(string='Tipo de Trabajador')
    jornada_semana_reducida = fields.Char(string='Jornada/Semana Reducida')
    fecha_de_alta = fields.Char(string='Fecha de Alta')
    salario_diario_integrado = fields.Char(string='Salario Diario Integrado')
    clave_de_ubicacion = fields.Char(string='Clave De Ubicacion',default=CLAVE_DE_UBICACION)
    numero_de_credito_infonavit = fields.Char(string='Número De Crédito Infonavit')
    fecha_de_inicio_de_descuento = fields.Char(string='Fecha de Inicio de Descuento')
    tipo_de_descuento = fields.Char(string='Tipo de Descuento')
    valor_de_descuento = fields.Char(string='Valor De Descuento')
    tipo_de_pension = fields.Char(string='Tipo de Pension')
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

    @api.constrains('fecha_de_alta')
    def _check_long_8(self):
        print(self)

    @api.constrains('salario_diario_integrado')
    def _check_long_7(self):
        print(self)

    @api.constrains('clave_de_ubicacion')
    def _check_long_17(self):
        print(self)

    @api.one
    def _check_long_10(self):
        CREDITO_INFONAVIT = True if self.numero_de_credito_infonavit else  False
        if CREDITO_INFONAVIT:
            self.__ev_long(self.numero_de_credito_infonavit,LONG10)
            self.__ev_long(self.fecha_de_inicio_de_descuento,LONG8)
            self.__ev_long(self.tipo_de_descuento,LONG1)
            self.__ev_long(self.valor_de_descuento,LONG8)
        elif not CREDITO_INFONAVIT:
            self.numero_de_credito_infonavit=self.fill_empty_or_incomplete(FILLSPACE,LONG10,REPLACERIGHT)
            self.fecha_de_inicio_de_descuento=self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT)
            self.tipo_de_descuento=self.fill_empty_or_incomplete(FILLZERO,LONG1,REPLACERIGHT)
            self.valor_de_descuento=self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT)



    @api.constrains('tipo_de_pension','tipo_de_trabajador','jornada_semana_reducida')
    def _check_long_1(self):
        print(self)

    @api.one
    def __ev_long(self,field_value,long,field_name="Test"):
        if CREDITO_INFONAVIT:
            if not len(field_value) == long:
                raise ValidationError("El Campo ${field_name} debe contener ${long} Carácteres")

    
    def fill_empty_or_incomplete(self,char_to_fill,long,position,original_char=""):
        if len(original_char)==long:
            return original_char
        elif position=="left":
            return original_char.ljust(long,char_to_fill)
        elif position=="right":
            return original_char.ljust(long,char_to_fill)
         



    @api.model
    def create(self, values):
        res = super(SUAAseg, self).create(values)
        res._check_long_10()
        return res



# === Computed Fields Methods ===
    @api.depends('nombre','apellido_paterno','apellido_materno')
    def _compute_nombre_apellidopaterno_materno_nombre(self):
        pass