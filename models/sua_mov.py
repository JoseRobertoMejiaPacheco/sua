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
    'nombre_apellidopaterno_materno_nombre',
    'clave_de_ubicacion','clave_de_municipio','clave_lugar_de_nacimiento','sexo']
FIELDS_TO_STRIP=['registro_patronal_imss','reg_fed_de_contribuyentes','curp',
    'nombre','apellido_paterno','apellido_materno','clave_de_municipio','ocupacion','clave_lugar_de_nacimiento','sexo','salario_diario_integrado_sua']
DEFAULT_NUMERO_CREDITO_INFONAVIT='          '



class SUAMov(models.Model):
    _name = 'sua.mov'
    _description = 'Formato del Archivo de Importación de Movimientos de Trabajadores MOVS.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal',default= lambda self: self.env.user.company_id.registro_patronal or FILLSPACE,size=LONG11)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social',size=LONG11)
    tipo_de_movimiento = fields.Selection(string='Tipo de Movimiento', selection=[('02', 'Baja'), ('07', 'Modificación de Salario'),
    ('08', 'Reingreso'),('09', 'Aportación Voluntaria'),('11', 'Ausentismo'),('12', 'Incapacidad')])
    fecha_de_movimiento = fields.Char(string='Fecha del Movimiento',size=LONG8)
    folio_de_incapacidad = fields.Char(string='Folio de Incapacidad',size=LONG8)
    dias_de_la_incidencia = fields.Char(string='Días de la Incidencia',size=LONG2)
    dias_de_la_incidencia_formato_sua = fields.Char(compute='_compute_dias_de_la_incidencia_formato_sua', string='Días de Incidencia Formato SUA')
    salario_diario_integrado = fields.Char(string='Salario Diario Integrado',size=LONG7,help="""El Salario Diario Integrado (5 enteros y 2 decimales) debe grabarse SIN punto decimal y rellenando con ceros a la
izquierda (ejemplo: para el salario 150.45, se debe asignar 0015045).""")
    salario_diario_integrado_sua = fields.Char(compute='_compute_salario_diario_integrado_sua',string='Salario Diario Integrado Formato SUA o Aportacion Voluntaria')
    complete_row_afil = fields.Char(string='Registro Completo para Formato SUA Movs.txt')
    
    
    @api.depends('dias_de_la_incidencia')
    def _compute_dias_de_la_incidencia_formato_sua(self):
        self.dias_de_la_incidencia_formato_sua = self.fill_empty_or_incomplete(FILLZERO,LONG2,REPLACELEFT,self.dias_de_la_incidencia or FILLEMPTY)
     

    @api.constrains('salario_diario_integrado_sua')
    def _check_long_7(self):
        self.__ev_long(LONG7,self.salario_diario_integrado_sua,self._fields['salario_diario_integrado_sua'])

    @api.one
    @api.constrains('fecha_de_movimiento')
    def _check_fecha_de_nacimiento(self):
        self.__ev_long(LONG8,self.fecha_de_movimiento,self._fields['fecha_de_movimiento'])

    @api.one
    @api.constrains('folio_de_incapacidad')
    def _check_folio_de_incapacidad(self):
        self.__ev_long(LONG8,self.folio_de_incapacidad,self._fields['folio_de_incapacidad'])

    @api.one
    @api.constrains('numero_de_seguridad_social')
    def _check_numero_de_seguridad_social(self):
        self.__ev_long(LONG11,self.numero_de_seguridad_social,self._fields['numero_de_seguridad_social'])

    @api.one
    @api.constrains('registro_patronal_imss')
    def _check_registro_patronal_imss(self):
        self.__ev_long(LONG11,self.registro_patronal_imss,self._fields['registro_patronal_imss'])


    
    @api.depends('salario_diario_integrado')
    def _compute_salario_diario_integrado_sua(self):
        if self.salario_diario_integrado:
            string_value = self.salario_diario_integrado.replace('.', '')
            removing_dot = string_value if  self.salario_diario_integrado else True
            self.salario_diario_integrado_sua=self.fill_empty_or_incomplete(FILLZERO,LONG7,REPLACELEFT,removing_dot)
        else:
            self.salario_diario_integrado_sua=self.fill_empty_or_incomplete(FILLZERO,LONG7,REPLACELEFT,FILLEMPTY)

# === Complete with spaces or 0, nothing must be null or incomplete  sua.aseg for template of ASEG.txt===
    def fill_empty_or_incomplete(self,char_to_fill,long,position,original_char=""):
        """Fills a string with a specific character, and long at left or right position"""
        if len(original_char)==long:
            return original_char
        elif position=="left":
            a = original_char.rjust(long,char_to_fill)
            print(a)
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
                string = string.strip()            
        else:
            if key in FIELDS_TO_STRIP:
                string = string.strip()
        return string

    @api.model
    def create(self, values):
        res =  super(SUAMov, self).create(self.remove_spaces_and_upper_case(values))
        res._check_tipo_de_movimiento()

    @api.multi
    def write(self, values):
        res = super(SUAMov, self).write(self.remove_spaces_and_upper_case(values))
        self._check_tipo_de_movimiento()
        return res

    @api.multi
    def get_full_row_MOV(self):
        return self.registro_patronal_imss+self.numero_de_seguridad_social+self.tipo_de_movimiento+self.fecha_de_movimiento+\
            self.fill_empty_or_incomplete(FILLSPACE,LONG8,REPLACELEFT,self.folio_de_incapacidad or FILLEMPTY)+self.dias_de_la_incidencia_formato_sua+self.salario_diario_integrado_sua


    @api.one
    def get_complete_row_afil(self):
        self.complete_row_afil=self.get_full_row_MOV()

    @api.one
    def unlink(self):
        print(self.get_complete_row_afil())
        print(len(self.get_complete_row_afil()))

    
    @api.one
    def _check_tipo_de_movimiento(self):
        if self.tipo_de_movimiento in ['12']:
            if self.folio_de_incapacidad==(FILLSPACE*8):
                raise ValidationError("El Campo folio_de_incapacidad es requerido para el tipo de movimiento"+self.tipo_de_movimiento)  

        if self.tipo_de_movimiento in ['12','11']:
            if self.dias_de_la_incidencia_formato_sua==(FILLZERO*2):
                raise ValidationError("El Campo dias_de_la_incidencia_formato_sua es requerido para el tipo de movimiento"+self.tipo_de_movimiento)

        if self.tipo_de_movimiento in ['07','08']:
            if self.salario_diario_integrado_sua==(FILLZERO*7):
                raise ValidationError("El Campo salario_diario_integrado_sua es requerido para el tipo de movimiento"+self.tipo_de_movimiento)

            
    