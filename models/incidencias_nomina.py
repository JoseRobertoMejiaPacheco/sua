from odoo import _, api, fields, models



class IncidenciasNomina(models.Model):
    _inherit = 'incidencias.nomina'
    sua_mov_id = fields.Many2one('sua.mov', string='Movimientos SUA')
    
    @api.multi
    def action_validar(self):
        employee = self.employee_id
        vals_base = {'registro_patronal_imss':employee.company_id.registro_patronal,                                   
                                    'numero_de_seguridad_social':employee.segurosocial,                                   
                                    'fecha_de_movimiento':fields.Datetime.from_string(self.fecha).strftime("%d%m%Y")}
       
        if employee:
            if self.tipo_de_incidencia=='Cambio reg. patronal':
                employee.write({'registro_patronal':self.registro_patronal})
            elif self.tipo_de_incidencia=='Cambio salario':
                if employee.contract_ids:
                    employee.contract_ids[0].write({'wage':self.sueldo_mensual,
                                                    'sueldo_diario_integrado' : self.sueldo_diario_integrado,
                                                    'sueldo_base_cotizacion' : self.sueldo_cotizacion_base,
                                                    'sueldo_integrado':self.sueldo_liquidacion_4g,
                                                    'sueldo_diario' : self.sueldo_diario,
                                                    'sueldo_hora' : self.sueldo_por_horas
                                                    })
                    self.env['contract.historial.salario'].create({'sueldo_mensual': self.sueldo_mensual, 'sueldo_diario': self.sueldo_diario, 'fecha_sueldo': self.fecha,
                                                                   'sueldo_por_hora' : self.sueldo_por_horas, 'sueldo_diario_integrado': self.sueldo_diario_integrado,
                                                                   'sueldo_base_cotizacion': self.sueldo_cotizacion_base, 'contract_id' : employee.contract_ids[0].id,
                                                                   'sueldo_liquidacion_4g': self.calculate_sueldo_liquidacion_4g(),
                                                                   })
                                                                
                    vals_base.update({'salario_diario_integrado':self.sua_mov_id.salario_diario_integrado_dos_decimales(self.sueldo_diario_integrado),'tipo_de_movimiento':'07'})
                    rec = self.sua_mov_id.create(vals_base)
                    rec.get_complete_row_afil()
                    self.sua_mov_id = rec.id
                    
                    print(self.sua_mov_id)

            elif self.tipo_de_incidencia=='Baja':
                vals_base.update({'tipo_de_movimiento':'02' })
                rec = self.sua_mov_id.create(vals_base)
                self.sua_mov_id = rec.id
                employee.write({'active':False})
                if employee.contract_ids:
                    employee.contract_ids.write({'state':'cancel'})
            elif self.tipo_de_incidencia=='Reingreso':
                employee.write({'active':True, 'registro_patronal': self.registro_patronal})
                if employee.contract_ids:
                    employee.contract_ids[0].write({'state':'open',
                                                 'sueldo_diario' : self.sueldo_diario,
                                                 'wage' : self.sueldo_mensual,
                                                 'sueldo_diario_integrado' : self.sueldo_diario_integrado,
                                                 'sueldo_base_cotizacion' : self.sueldo_cotizacion_base,
                                                 'sueldo_hora': self.sueldo_por_horas
                                                 })
                    self.env['contract.historial.salario'].create({'sueldo_mensual': self.sueldo_mensual, 'sueldo_diario': self.sueldo_diario, 'fecha_sueldo': self.fecha,
                                                                   'sueldo_por_hora' : self.sueldo_por_horas, 'sueldo_diario_integrado': self.sueldo_diario_integrado,
                                                                   'sueldo_base_cotizacion': self.sueldo_cotizacion_base, 'contract_id' : employee.contract_ids[0].id,
                                                                   'sueldo_liquidacion_4g': self.calculate_sueldo_liquidacion_4g(),
                                                                   })
                    vals_base.update({'salario_diario_integrado':"{:.2f}".format((self.sueldo_diario_integrado)),'tipo_de_movimiento':'08'})
                    rec = self.sua_mov_id.create(vals_base)
                    self.sua_mov_id = rec.id
                    rec.get_complete_row_afil()
        self.state='done'
        return
    


    @api.multi
    def unlink(self):
        for item in self:
            if item.sua_mov_id:
                item.sua_mov_id.unlink()                
        return models.Model.unlink(self)