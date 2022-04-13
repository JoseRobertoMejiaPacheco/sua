from models.sua_mov_cr import FILLSPACE
from odoo import _, api, fields, models
from odoo import tools, _

class Employee(models.Model):
    _inherit = 'hr.employee'
    names = fields.Char(string='Nombre(s)')
    first_name = fields.Char(string='Apellido Paterno')
    second_name = fields.Char(string='Apellido Materno')

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