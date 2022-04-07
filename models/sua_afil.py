from email.policy import default
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError,RedirectWarning
from datetime import datetime
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



class SUAAfil(models.Model):
    _name = 'sua.afil'
    _description = 'Formato del Archivo de Importación de Trabajadores AFIL.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal',default= lambda self: self.env.user.company_id.registro_patronal or FILLSPACE,size=LONG11)
    digito_verificador_registro_patronal = fields.Char(string='Dígito Verificador Registro Patronal',size=LONG1)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social',size=LONG11,default=FILLSPACE)
    digito_verificador_numero_de_seguridad_social = fields.Char(string='Dígito Verificador Número de Seguridad Social')
    codigo_postal = fields.Char(string='Código Postal',size=LONG5)
    fecha_de_nacimiento = fields.Char(string='Fecha de Nacimiento',size=LONG8)
    lugar_de_nacimiento = fields.Many2one('sua.estados', string='Lugar de Nacimiento')
    unidad_de_medicina_familiar = fields.Char(string='Unidad de Medicina Familar',size=LONG3)
    clave_lugar_de_nacimiento = fields.Char(string='Clave del lugar de nacimiento',size=LONG2)
    ocupacion = fields.Char(string='Ocupación',size=LONG12)
    sexo = fields.Selection(string='Sexo', selection=[('M', 'Masculino'), ('F', 'Femenino')])
    tipo_de_salario = fields.Selection(string='Tipo de Salario', selection=[('0', 'Fijo'), ('1', 'Variable'),('2', 'Mixto')])
    hora = fields.Char(string='Hora',size=LONG1)

    complete_row_afil = fields.Char(string='Registro Completo para Formato SUA Afil.txt')


    @api.onchange('lugar_de_nacimiento')
    def _onchange_lugar_de_nacimiento(self):
        self.clave_lugar_de_nacimiento = self.lugar_de_nacimiento.cve_curp

    @api.onchange('numero_de_seguridad_social')
    def _onchange_numero_de_seguridad_social(self):
        if len(self.numero_de_seguridad_social)==LONG11:
            self.digito_verificador_numero_de_seguridad_social=self.numero_de_seguridad_social[-1]

    @api.onchange('registro_patronal_imss')
    def _onchange_registro_patronal_imss(self):
        if len(self.registro_patronal_imss)==LONG11:
            self.digito_verificador_registro_patronal=self.registro_patronal_imss[-1]
    
    @api.one
    @api.constrains('registro_patronal_imss')
    def _check_registro_patronal_imss(self):
        self.__ev_long(LONG11,self.registro_patronal_imss,self._fields['registro_patronal_imss'])

    @api.one
    @api.constrains('digito_verificador_registro_patronal')
    def _check_digito_verificador_registro_patronal(self):
        self.__ev_long(LONG1,self.digito_verificador_registro_patronal,self._fields['digito_verificador_registro_patronal'])
    @api.one
    @api.constrains('numero_de_seguridad_social')
    def _check_numero_de_seguridad_social(self):
        self.__ev_long(LONG11,self.numero_de_seguridad_social,self._fields['numero_de_seguridad_social'])

    @api.one
    @api.constrains('digito_verificador_numero_de_seguridad_social')
    def _check_digito_verificador_numero_de_seguridad_social(self):
        self.__ev_long(LONG1,self.digito_verificador_numero_de_seguridad_social,self._fields['digito_verificador_numero_de_seguridad_social'])

    @api.one
    @api.constrains('codigo_postal')
    def _check_codigo_postal(self):
        self.__ev_long(LONG5,self.codigo_postal,self._fields['codigo_postal'])
    
    @api.one
    @api.constrains('fecha_de_nacimiento')
    def _check_fecha_de_nacimiento(self):
        self.__ev_long(LONG8,self.fecha_de_nacimiento,self._fields['fecha_de_nacimiento'])
    
    @api.one
    @api.constrains('unidad_de_medicina_familiar')
    def _check_unidad_de_medicina_familiar(self):
        self.__ev_long(LONG3,self.unidad_de_medicina_familiar,self._fields['unidad_de_medicina_familiar'])

    @api.one
    @api.constrains('ocupacion')
    def _check_ocupacion(self):
        if isinstance(self.ocupacion, str):
            if len(self.ocupacion)<5:
                raise ValidationError("El Campo ocupacion debe contener al menos 5 Carácteres")
        else:
            raise ValidationError("El Campo ocupacion debe contener al menos 5 Carácteres pero está vacío.")


    @api.one
    @api.constrains('sexo')
    def _check_sexo(self):
        if not self.sexo:
            raise ValidationError("El Campo Sexo es requerido.")


    @api.one
    @api.constrains('lugar_de_nacimiento')
    def _check_lugar_de_nacimiento(self):
        if not self.lugar_de_nacimiento:
            self.__ev_long(LONG1,self.lugar_de_nacimiento,self._fields['lugar_de_nacimiento'])

    @api.one
    @api.constrains('tipo_de_salario')
    def _check_tipo_de_salario(self):
        self.__ev_long(LONG1,self.tipo_de_salario,self._fields['tipo_de_salario'])

    @api.one
    @api.constrains('hora')
    def _check_hora(self):
        self.__ev_long(LONG1,self.hora,self._fields['hora'])


    lugar_de_nacimiento_formato_sua = fields.Char(compute='_compute_lugar_de_nacimiento_formato_sua', string='Lugar de Nacimiento Formato SUA')

  

    @api.depends('lugar_de_nacimiento')
    def _compute_lugar_de_nacimiento_formato_sua(self):
        self.lugar_de_nacimiento_formato_sua = self.fill_empty_or_incomplete(FILLSPACE,LONG50,REPLACERIGHT,self.lugar_de_nacimiento.descripcion)

    ocupacion_formato_sua = fields.Char(compute='_compute_ocupacion_formato_sua', string='')
    
    @api.depends('ocupacion')
    def _compute_ocupacion_formato_sua(self):
        self.ocupacion_formato_sua = self.fill_empty_or_incomplete(FILLSPACE,LONG12,REPLACERIGHT,self.ocupacion)
    


# === Complete with spaces or 0, nothing must be null or incomplete  sua.aseg for template of ASEG.txt===
    def fill_empty_or_incomplete(self,char_to_fill,long,position,original_char=""):
        """Fills a string with a specific character, and long at left or right position"""
        if len(original_char)==long:
            return original_char
        elif position=="left":
            return original_char.rjust(long,char_to_fill)
        elif position=="right":
            return original_char.ljust(long,char_to_fill)        
        
# === Define Errors sua.aseg for template of ASEG.txt===
    @api.one
    def __ev_long(self,long,field_value="",field_name="undefined"):
        if isinstance(field_value, str):
            if not len(field_value) == long:
                raise ValidationError("El Campo {field_name} debe contener {long} Carácteres \n pero contiene {caracteres} Carácteres".format(field_name=field_name,long=long,caracteres=len(field_value)))
        else:
            raise ValidationError("El Campo {field_name} debe contener {long} Carácteres pero está vacío".format(field_name=field_name,long=long))  
    @api.model
    def create(self, values):
        values.update({'hora':int(datetime.now().strftime('%I'))})
        return super(SUAAfil, self).create(self.remove_spaces_and_upper_case(values))

    @api.multi
    def write(self, values):
        return super(SUAAfil, self).write(self.remove_spaces_and_upper_case(values))

    def remove_spaces_and_upper_case(self,dict):
        for key, value in dict.items():
            if key in dict.keys():
                if isinstance(value,str):
                    if not value.isdigit():
                        dict.update({key:self.remove_spaces_alum(value.upper(),key)})
        return dict

    def remove_spaces_alum(self,string,key=False):
        if string.isalnum():
            if key in FIELDS_TO_STRIP:
                return string.strip()            
        else:
            if key in FIELDS_TO_STRIP:
                return string.strip()
            else:
                return string

    @api.multi
    def get_full_row_AFIL(self):
        return self.registro_patronal_imss,self.digito_verificador_numero_de_seguridad_social,self.numero_de_seguridad_social,self.digito_verificador_numero_de_seguridad_social+\
            self.codigo_postal,self.fecha_de_nacimiento,self.lugar_de_nacimiento_formato_sua,self.clave_lugar_de_nacimiento,self.unidad_de_medicina_familiar,self.ocupacion_formato_sua,self.sexo+\
                self.tipo_de_salario,self.hora


    @api.one
    def get_complete_row_afil(self):

        self.complete_row_afil=self.get_full_row_AFIL()