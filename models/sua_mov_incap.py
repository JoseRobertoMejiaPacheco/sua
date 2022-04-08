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
    fecha_de_alta = fields.Char(string='Fecha de Alta')


    @api.constrains('fecha_de_alta')
    def _check_long_8(self):
        self.__ev_long(LONG8,self.fecha_de_alta,self._fields['fecha_de_alta'])

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
                    self.tipo_de_trabajador+self.jornada_semana_reducida+self.fecha_de_alta+\
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