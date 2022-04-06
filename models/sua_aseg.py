from email.policy import default
import string
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError,RedirectWarning

CLAVE_DE_UBICACION = '                 '
CREDITO_INFONAVIT = False
LONG10 = 10
LONG17 = 17
LONG1 = 1
LONG3 = 3
LONG4 = 4
LONG6 = 6
LONG13 = 13
LONG18 = 18
LONG50 = 50
LONG7 = 7
LONG8 = 8
LONG11 = 11
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
# === Model sua.aseg for template of ASEG.txt===
class SUAAseg(models.Model):
    _name = 'sua.aseg'
    _description = 'Formato del Archivo de Importación de Trabajadores ASEG.txt'
    registro_patronal_imss = fields.Char(string='Registro Patronal',default= lambda self: self.env.user.company_id.registro_patronal)
    numero_de_seguridad_social = fields.Char(string='Número de Seguridad Social')
    reg_fed_de_contribuyentes = fields.Char(string='Registro Ferederal de Contribuyentes')
    curp = fields.Char(string='CURP')
    nombre = fields.Char(string='Nombre(s) Separados por Espacio',help='Ejemplo Kaleth Chalino Valentin')
    apellido_paterno = fields.Char(string='Apellido Paterno')
    apellido_materno = fields.Char(string='Apellido Materno')
    nombre_apellidopaterno_materno_nombre = fields.Char(compute='_compute_nombre_apellidopaterno_materno_nombre', string='Nombre Completo Formato SUA')        
    tipo_de_trabajador = fields.Selection(
        string='Tipo de Trabajador',
        selection=[('1', 'Trab. permanente'), ('2', ' Trab. Ev. Ciudad'),('3', 'Trab. Ev. Construcción'),('4', 'Eventual del campo')]
    )
    jornada_semana_reducida = fields.Selection(
        string='Jornada/Semana Reducida',
        selection=[('1', 'Un día'), ('2', 'Dos dias'),('3', 'Trab. Ev. Construcción'),('4', 'Cuatros días'),
        ('5', 'Cinco días'),('6', 'Seis días'),('0', 'Jornada Normal')]
    )    
    fecha_de_alta = fields.Char(string='Fecha de Alta')

    
    salario_diario_integrado = fields.Char(string='Salario Diario Integrado')
    salario_diario_integrado_sua = fields.Char(compute='_compute_salario_diario_integrado_sua',string='Salario Diario Integrado Formato SUA')
    

    #api.one retorna new id
    
    @api.depends('salario_diario_integrado')
    def _compute_salario_diario_integrado_sua(self):
        if self.salario_diario_integrado:
            string_value = self.salario_diario_integrado.replace('.', '')
            removing_dot = string_value if  self.salario_diario_integrado else True
            self.salario_diario_integrado_sua=self.fill_empty_or_incomplete(FILLZERO,LONG7,REPLACELEFT,removing_dot)
        
        
    
    clave_de_ubicacion = fields.Char(string='Clave De Ubicacion',default=CLAVE_DE_UBICACION)
    numero_de_credito_infonavit = fields.Char(string='Número De Crédito Infonavit',default=DEFAULT_NUMERO_CREDITO_INFONAVIT)
    fecha_de_inicio_de_descuento = fields.Char(string='Fecha de Inicio de Descuento',default=lambda self :self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT))
    tipo_de_descuento = fields.Selection(
        string='Tipo de Descuento',
        selection=[('1', 'Porcentaje'),('2', 'Cuota Fija Monetaria'),('3', 'Factor de descuento'),('0', 'No Aplica')],
        default=' '
    )
    valor_de_descuento = fields.Char(string='Valor De Descuento',default=lambda self :self.fill_empty_or_incomplete(FILLZERO,LONG8,REPLACERIGHT),help="""
    1 Porcentaje (00EEDD00, dos enteros y dos decimales)
2 Cuota Fija Monetaria (EEEEEDD0, cinco enteros y dos decim ales)
3 Factor de Descuento (0EEEDDDD, tres enteros y cuatro decim ales)""")
    valor_de_descuento_sua = fields.Char(compute='_compute_valor_de_descuento',string='Valor De Descuento Formato SUA')
    

    # Todo Fix: Separar Constrains, si uno falla, fallan todos
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
    
    tipo_de_pension = fields.Selection(
        string='Tipo de Pension',
        selection=[('0', 'Sin Pensión'),('1', 'Pensión en Invalidez y Vida'),('2', 'Cesantía y Vejez')]
    )

    clave_de_municipio = fields.Char(string='Clave De Municipio',default= lambda self: self.env.user.company_id.registro_patronal[3:])



# === Onchange to Upper sua.aseg for template of ASEG.txt===
# style="text-transform:uppercase"

# === Constrains sua.aseg for template of ASEG.txt===
    @api.constrains('registro_patronal_imss','numero_de_seguridad_social')
    def _check_long_11(self):
        self.__ev_long(LONG11,self.registro_patronal_imss,self._fields['registro_patronal_imss'])
        self.__ev_long(LONG11,self.numero_de_seguridad_social,self._fields['numero_de_seguridad_social'])

    @api.constrains('reg_fed_de_contribuyentes')
    def _check_long_13(self):
        self.__ev_long(LONG13,self.reg_fed_de_contribuyentes,self._fields['reg_fed_de_contribuyentes'])

    @api.constrains('curp')
    def _check_long_18(self):
        self.__ev_long(LONG18,self.curp,self._fields['curp'])

    @api.constrains('nombre_apellidopaterno_materno_nombre')
    def _check_long_50(self):
        self.__ev_long(LONG50,self.nombre_apellidopaterno_materno_nombre,self._fields['nombre_apellidopaterno_materno_nombre'])

    @api.constrains('fecha_de_alta')
    def _check_long_8(self):
        self.__ev_long(LONG8,self.fecha_de_alta,self._fields['fecha_de_alta'])


    @api.constrains('clave_de_ubicacion')
    def _check_long_17(self):
        self.__ev_long(LONG17,self.clave_de_ubicacion,self._fields['clave_de_ubicacion'])

    @api.constrains('clave_de_municipio')
    def _check_long_3(self):
        self.__ev_long(LONG3,self.clave_de_municipio,self._fields['clave_de_municipio'])
    @api.one
    def _check_constrains_numero_de_credito_infonavit(self):
        """Constrains for main numero_de_credito_infonavit
        and derivated constains fecha_de_inicio_de_descuento,
        tipo_de_descuento, valor_de_descuento which
        only must be considerated when numero_de_credito_infonavit isn't empty."""
        """No asignar en constrains crea recursividad"""   

        self.__ev_long(LONG10,self.numero_de_credito_infonavit,self._fields['numero_de_credito_infonavit'])
        self.__ev_long(LONG8,self.fecha_de_inicio_de_descuento,self._fields['fecha_de_inicio_de_descuento'])
        self.__ev_long(LONG1,self.tipo_de_descuento,self._fields['tipo_de_descuento'])
        self.__ev_long(LONG8,self.valor_de_descuento_sua,self._fields['valor_de_descuento_sua'])





    @api.constrains('tipo_de_pension','tipo_de_trabajador','jornada_semana_reducida')
    def _check_long_1(self):
        self.__ev_long(LONG1,self.tipo_de_pension,self._fields['tipo_de_pension'])
        self.__ev_long(LONG1,self.tipo_de_trabajador,self._fields['tipo_de_trabajador'])
        self.__ev_long(LONG1,self.jornada_semana_reducida,self._fields['jornada_semana_reducida'])
    
    @api.constrains('salario_diario_integrado')
    def _check_long_7(self):
        self.__ev_long(LONG7,self.salario_diario_integrado_sua,self._fields['salario_diario_integrado_sua'])
            
    

    


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
        res = super(SUAAseg, self).create(self.remove_spaces_and_upper_case(values))
        res._check_constrains_numero_de_credito_infonavit()
        print(self.get_full_row_ASEG())
        print(len(self.get_full_row_ASEG()))
        return res

    @api.multi
    def write(self, values):
        """"update values for new"""
        res= super(SUAAseg, self).write(self.remove_spaces_and_upper_case(values))
        self._check_constrains_numero_de_credito_infonavit()
        print(self.get_full_row_ASEG())
        print(len(self.get_full_row_ASEG()))
        # if 'salario_diario_integrado' in values.keys():
        #     self._compute_salario_diario_integrado_sua()
    
    def remove_spaces_and_upper_case(self,dict):
        for key, value in dict.items():
            if key in dict.keys():
                if isinstance(value,str):
                    if not value.isdigit():
                        dict.update({key:self.remove_spaces_alum(value.upper(),key)})
        return dict


    @api.one
    def get_full_row_ASEG(self):
        if self:
            return self.registro_patronal_imss+self.numero_de_seguridad_social+\
                self.reg_fed_de_contribuyentes+self.curp+self.nombre_apellidopaterno_materno_nombre+\
                    self.tipo_de_trabajador+self.jornada_semana_reducida+self.fecha_de_alta+\
                        self.salario_diario_integrado_sua+self.clave_de_ubicacion+self.numero_de_credito_infonavit+\
                            self.fecha_de_inicio_de_descuento+self.tipo_de_descuento+self.valor_de_descuento_sua+self.tipo_de_pension+self.clave_de_municipio

    def remove_spaces_alum(self,string,key=False):
        if string.isalnum():
            if key in FIELDS_TO_STRIP:
                return string.strip()            
        else:
            if key in FIELDS_TO_STRIP:
                return string.strip()
            else:
                return string
            


# === Computed Fields Methods ===
    @api.one
    @api.depends('nombre','apellido_paterno','apellido_materno')
    def _compute_nombre_apellidopaterno_materno_nombre(self):
        try:                        
            if not self.apellido_paterno:
                full_name_formatted=self.apellido_materno+NAME_SEPARATOR+NAME_SEPARATOR+self.nombre
                self.nombre_apellidopaterno_materno_nombre = self.fill_empty_or_incomplete(FILLSPACE,LONG50,REPLACERIGHT,full_name_formatted)                
            else:
                full_name_formatted = self.apellido_paterno+NAME_SEPARATOR+self.apellido_materno+NAME_SEPARATOR+self.nombre
                self.nombre_apellidopaterno_materno_nombre = self.fill_empty_or_incomplete(FILLSPACE,LONG50,REPLACERIGHT,full_name_formatted)                
        except Exception as inst:
            print(inst)

        


