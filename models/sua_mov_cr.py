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



class SUAMovCr(models.Model):
    _name = 'sua.mov.cr'
    _description = 'Formato del Archivo de Importación de Movimientos de Crédito SUAMOVCR.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal',default= lambda self: self.env.user.company_id.registro_patronal or FILLSPACE,size=LONG11)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social',size=LONG11)
    numero_de_credito_infonavit = fields.Char(string='Número De Crédito Infonavit',default=DEFAULT_NUMERO_CREDITO_INFONAVIT)
    tipo_de_movimiento = fields.Selection(string='Tipo de Movimiento', selection=[('15', 'Inicio de Crédito de Vivienda (ICV)'), ('16', 'Fecha de Suspensión de Descuento (FS)'),
    ('17', 'Reinicio de Descuento (RD)'),('18', 'Modificación de Tipo de Descuento (MTD)'),('19', 'Modificación de Valor de Descuento (MVD)'),('20', 'Modificación de Número de Crédito (MND)')])
    fecha_de_movimiento = fields.Char(string='Fecha de Inicio de Descuento',default=lambda self :self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT))
    tipo_de_descuento = fields.Selection(
        string='Tipo de Descuento',
        selection=[('1', 'Porcentaje'),('2', 'Cuota Fija Monetaria'),('3', 'Factor de descuento'),('0', 'No Aplica')],
        default='0'
    )
    valor_de_descuento = fields.Char(string='Valor De Descuento',default=lambda self :self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT),help="""
    1 Porcentaje (00EEDD00, dos enteros y dos decimales)
2 Cuota Fija Monetaria (EEEEEDD0, cinco enteros y dos decim ales)
3 Factor de Descuento (0EEEDDDD, tres enteros y cuatro decim ales)""")
    aplica_tabla_disminucion_de_porcentaje = fields.Selection(string='Aplica Tabla Disminución de %', selection=[('S', 'Si'), ('N', 'No')])
    complete_row_afil = fields.Char(string='Registro Completo para Formato SUA Movs.txt')
    
    @api.depends('dias_de_la_incidencia')
    def _compute_dias_de_la_incidencia_formato_sua(self):
        self.dias_de_la_incidencia_formato_sua = self.fill_empty_or_incomplete(FILLZERO,LONG2,REPLACELEFT,self.dias_de_la_incidencia or FILLEMPTY)
     
    @api.constrains('')
    def _check_(self):
        self.numero_de_credito_infonavit = self.fill_empty_or_incomplete(FILLSPACE,LONG10,REPLACERIGHT)

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

    @api.one
    @api.depends('valor_de_descuento','tipo_de_descuento')
    def _compute_valor_de_descuento(self):
        if self.tipo_de_descuento=='1':
            if len(self.valor_de_descuento) == LONG4:
                self.valor_de_descuento_sua=FILLZERO*2+self.valor_de_descuento+FILLZERO*2
        elif self.tipo_de_descuento=='2':
            if len(self.valor_de_descuento) == LONG7:
                self.valor_de_descuento_sua = self.valor_de_descuento+FILLZERO
        elif self.tipo_de_descuento=='3':
            if len(self.valor_de_descuento) == LONG7:
                self.valor_de_descuento_sua=FILLZERO+self.valor_de_descuento
        else:
            self.valor_de_descuento
            self.valor_de_descuento_sua =self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT)
            self.fecha_de_inicio_de_descuento = self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT)            
            self.numero_de_credito_infonavit = self.fill_empty_or_incomplete(FILLSPACE,LONG10,REPLACERIGHT)
            self.tipo_de_descuento = self.fill_empty_or_incomplete(FILLZERO,LONG1,REPLACERIGHT)
            self.valor_de_descuento = self.fill_empty_or_incomplete(FILLZERO,LONG1,REPLACERIGHT)
    
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
        print(key)
        if string.isalnum():
            if key in FIELDS_TO_STRIP:
                string = string.strip()            
        else:
            if key in FIELDS_TO_STRIP:
                string = string.strip()
        return string

    @api.model
    def create(self, values):
        return  super(SUAMovCr, self).create(self.remove_spaces_and_upper_case(values))
       

    @api.multi
    def write(self, values):
        res = super(SUAMovCr, self).write(self.remove_spaces_and_upper_case(values))
        
        return res

    @api.multi
    def get_full_row_MOV(self):
        return self.registro_patronal_imss+self.numero_de_seguridad_social+self.numero_de_credito_infonavit+self.tipo_de_movimiento+self.fecha_de_movimiento+\
            self.tipo_de_descuento+self.valor_de_descuento+self.aplica_tabla_disminucion_de_porcentaje


    @api.one
    def get_complete_row_afil(self):
        self.complete_row_afil=self.get_full_row_MOV()

    @api.one
    def unlink(self):
        print(self.get_complete_row_afil())
        print(len(self.get_complete_row_afil()))

    

    @api.one
    def _check_constrains_numero_de_credito_infonavit(self):
        """Constrains for main numero_de_credito_infonavit
        and derivated constains fecha_de_movimiento,
        tipo_de_descuento, valor_de_descuento which
        only must be considerated when numero_de_credito_infonavit isn't empty."""
        """No asignar en constrains crea recursividad"""   

        self.__ev_long(LONG10,self.numero_de_credito_infonavit,self._fields['numero_de_credito_infonavit'])
        self.__ev_long(LONG8,self.fecha_de_movimiento,self._fields['fecha_de_movimiento'])
        self.__ev_long(LONG1,self.tipo_de_descuento,self._fields['tipo_de_descuento'])
        self.__ev_long(LONG8,self.valor_de_descuento_sua,self._fields['valor_de_descuento_sua'])       
    