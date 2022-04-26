from odoo import _, api, fields, models
from odoo import tools, _

class Employee(models.Model):
    _inherit = 'hr.employee'
    names = fields.Char(string='Nombre(s)')
    first_name = fields.Char(string='Apellido Paterno')
    second_name = fields.Char(string='Apellido Materno')
    state_sua_idse = fields.Selection(string='Estado de Registro SUA/IDSE',selection=[
            ('normal', 'In Progress'),
            ('blocked', 'Blocked'),
            ('done', 'Ready for next stage')],default='normal')
    aseg_id = fields.Many2one('sua.aseg', string='Aseg ID')
    
    @api.model
    def create(self, vals):
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        tools.image_resize_images(vals)
        return super(Employee, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'address_home_id' in vals:
            account_id = vals.get('bank_account_id') or self.bank_account_id.id
            if account_id:
                self.env['res.partner.bank'].browse(account_id).partner_id = vals['address_home_id']
        tools.image_resize_images(vals)
        if all(key in vals for key in ("names","first_name","second_name")):            
            complete_name = str(vals.get('names') or self.names or '')+' '+ str(vals.get('first_name') or self.first_name or '')+' '+str(vals.get('second_name') or self.second_name or '')
            vals.update({'name':complete_name})
        res = super(Employee, self).write(vals)
        return res
    
    @api.one
    def create_complete_row_afil(self):
        
        vals = {
            'registro_patronal_imss':self.company_id.registro_patronal,
            'numero_de_seguridad_social':self.segurosocial,
            'reg_fed_de_contribuyentes':self.rfc,
            'curp':self.curp,
            'nombre':self.names,
            'apellido_paterno':self.first_name,
            'apellido_materno':self.second_name,
            'fecha_de_alta':fields.Datetime.from_string(self.contract_id.date_start).strftime("%d%m%Y"),
            'salario_diario_integrado':"{:.2f}".format((self.contract_id.sueldo_diario_integrado)) ,
            'numero_de_credito_infonavit':self.cred_infonavit or '0000000000',
            'fecha_de_inicio_de_descuento':'00000000', #usar or para la fecha de inicio de descuento
            'tipo_de_descuento':  '0',#usar or            
            'clave_de_municipio':self.env.user.company_id.registro_patronal[:3]        
        }
        aseg = self.env['sua.aseg'].create(vals)
        self.aseg_id = aseg.id
        