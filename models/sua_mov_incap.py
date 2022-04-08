from email.policy import default
from os import unlink
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
LONG25 = 25
LONG7 = 7
LONG8 = 8
LONG11 = 11
LONG12 = 12
FILLZERO = "0"
FILLEMPTY = ""
FILLSPACE = " "
REPLACELEFT = 'left'
REPLACERIGHT = 'right'
NAME_SEPARATOR = '$'
FIELDS_TO_UPPER_CASE=[
    'registro_patronal_imss','reg_fed_de_contribuyentes','curp',
    'nombre','apellido_paterno','apellido_materno',
    'nombre_apellidopaterno_materno_nombre','aplica_tabla_disminucion_de_porcentaje',
    'clave_de_ubicacion','clave_de_municipio','clave_lugar_de_nacimiento','sexo']
FIELDS_TO_STRIP=['registro_patronal_imss','reg_fed_de_contribuyentes','curp','aplica_tabla_disminucion_de_porcentaje',
    'nombre','apellido_paterno','apellido_materno','clave_de_municipio','ocupacion','clave_lugar_de_nacimiento','sexo','salario_diario_integrado_sua']
DEFAULT_NUMERO_CREDITO_INFONAVIT='          '



class SUAMovIncap(models.Model):
    _name = 'sua.mov.incap'
    _description = 'Formato del Archivo de Importación de Movimientos de Crédito INCAP.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal',default= lambda self: self.env.user.company_id.registro_patronal or FILLSPACE,size=LONG11)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social',size=LONG11)
    tipo_de_incidencia = fields.Char(string='Tipo de Incidencia',default='1')
    fecha_de_inicio = fields.Char(string='Fecha de Alta')
    folio = fields.Char(string='Folio de Incapacidad',size=LONG8)
    dias_subsidiados = fields.Char(string='Días Subsidiados',size=LONG3)
    rama_de_incapacidad = fields.Char(string='Rama de Incapacidad')
    tipo_de_riesgo = fields.Char(string='Tipo de Riesgo')
    secuela_o_consecuencia = fields.Char(string='Secuela o Consecuencia')
    control_de_incapacidad = fields.Char(string='Control de Incapacidad')
    fecha_de_termino = fields.Char(string='Fecha de Término')


    @api.constrains('fecha_de_termino')
    def _check_long_fecha_de_inicio(self):
        self.__ev_long(LONG8,self.fecha_de_termino,self._fields['fecha_de_termino'])

    @api.one
    @api.constrains('control_de_incapacidad')
    def _check_control_de_incapacidad(self):
        self.__ev_long(LONG1,self.control_de_incapacidad,self._fields['control_de_incapacidad'])

    @api.one
    @api.constrains('secuela_o_consecuencia')
    def _check_secuela_o_consecuencia(self):
        self.__ev_long(LONG1,self.secuela_o_consecuencia,self._fields['secuela_o_consecuencia'])

    @api.one
    @api.constrains('tipo_de_riesgo')
    def _check_rama_de_incapacidad(self):
        self.__ev_long(LONG1,self.tipo_de_riesgo,self._fields['tipo_de_riesgo'])

    @api.one
    @api.constrains('rama_de_incapacidad')
    def _check_rama_de_incapacidad(self):
        self.__ev_long(LONG1,self.rama_de_incapacidad,self._fields['rama_de_incapacidad'])

    @api.one
    @api.constrains('dias_subsidiados')
    def _check_dias_subsidiados(self):
        self.__ev_long(LONG8,self.dias_subsidiados,self._fields['dias_subsidiados'])

    @api.one
    @api.constrains('folio')
    def _check_folio(self):
        self.__ev_long(LONG8,self.folio,self._fields['folio'])

    @api.constrains('fecha_de_inicio')
    def _check_long_fecha_de_inicio(self):
        self.__ev_long(LONG8,self.fecha_de_inicio,self._fields['fecha_de_inicio'])

    @api.constrains('tipo_de_incidencia')
    def _check_long_tipo_de_incidencia(self):
        self.__ev_long(LONG8,self.tipo_de_incidencia,self._fields['tipo_de_incidencia'])

# === Define Errors sua.aseg for template of ASEG.txt===
    @api.one
    def __ev_long(self,long,field_value="",field_name="undefined"):
        if isinstance(field_value, str):
            if not len(field_value) == long:
                raise ValidationError("El Campo {field_name} debe contener {long} Carácteres \n pero contiene {caracteres} Carácteres".format(field_name=field_name,long=long,caracteres=len(field_value)))
        else:
            raise ValidationError("El Campo {field_name} debe contener {long} Carácteres pero está vacío".format(field_name=field_name,long=long))   

            
    

# === Complete with spaces or 0, nothing must be null or incomplete  sua.aseg for template of ASEG.txt===
    def fill_empty_or_incomplete(self,char_to_fill,long,position,original_char=""):
        """Fills a string with a specific character, and long at left or right position"""
        if len(original_char)==long:
            return original_char
        elif position=="left":
            return original_char.rjust(long,char_to_fill)
        elif position=="right":
            return original_char.ljust(long,char_to_fill)
         



# === Override ORM Methods sua.aseg for template of ASEG.txt===
    @api.model
    def create(self, values):
        res = super(SUAMovIncap, self).create(self.remove_spaces_and_upper_case(values))
        res._check_constrains_numero_de_credito_infonavit()
        return res

    @api.multi
    def write(self, values):
        """"update values for new"""
        res= super(SUAMovIncap, self).write(self.remove_spaces_and_upper_case(values))
        self._check_constrains_numero_de_credito_infonavit()
     
    
    def remove_spaces_and_upper_case(self,dict):
        for key, value in dict.items():
            if key in dict.keys():
                if isinstance(value,str):
                    if not value.isdigit():
                        dict.update({key:self.remove_spaces_alum(value.upper(),key)})
        return dict


    @api.multi
    def get_full_row_ASEG(self):
        if self.ensure_one():
            return self.registro_patronal_imss+self.numero_de_seguridad_social+\
                self.reg_fed_de_contribuyentes+self.curp+self.nombre_apellidopaterno_materno_nombre+\
                    self.tipo_de_trabajador+self.jornada_semana_reducida+self.fecha_de_inicio+\
                        self.salario_diario_integrado_sua+self.clave_de_ubicacion+self.numero_de_credito_infonavit+\
                            self.fecha_de_inicio_de_descuento+self.tipo_de_descuento+self.valor_de_descuento_sua+self.tipo_de_pension+self.clave_de_municipio

    def remove_spaces_alum(self,string,key=False):
        if string.isalnum():
            if key in FIELDS_TO_STRIP:
                string = string.strip()            
        else:
            if key in FIELDS_TO_STRIP:
                string = string.strip()
        return string

    @api.one
    def get_complete_row_aseg(self):
        self.complete_row_aseg=self.get_full_row_ASEG()