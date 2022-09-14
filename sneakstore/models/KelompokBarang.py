from odoo import api, fields, models


class KelompokBarang(models.Model):
    _name = 'sneakstore.kelompokbarang'
    _description = 'New Description'

    name = fields.Selection([
        ('nike', 'Nike'), 
        ('adidas', 'Adidas'), 
        ('puma', 'Puma'),
        ('onitsuka', 'Onitsuka'),
        ('rebook', 'Rebook')        
    ], string='Brand')

    kode_kelompok = fields.Char(string='Code')
    
        
    @api.onchange('name')
    def _onchange_kode_kelompok(self):
        if (self.name == 'nike'):
            self.kode_kelompok = 'nike'
        elif (self.name == 'adidas'):
            self.kode_kelompok = 'adidas'
        elif (self.name == 'puma'):
            self.kode_kelompok = 'puma'
        elif (self.name == 'onitsuka'):
            self.kode_kelompok = 'onitsuka'
        elif (self.name == 'rebook'):
            self.kode_kelompok = 'rebook'

    kode_rak = fields.Selection([
        ('rak_nike', 'rak_Nike'), 
        ('rak_adidas', 'rak_Adidas'), 
        ('rak_puma', 'rak_Puma'),
        ('rak_onitsuka', 'rak_Onitsuka'),
        ('rak_rebook', 'rak_Rebook')        
    ], string='Rack')
    barang_ids = fields.One2many(comodel_name='sneakstore.barang', 
                                inverse_name='kelompokbarang_id', 
                                string='Sneakers List')
    jml_item = fields.Char(compute='_compute_jml_item', string='Total Item')
    
    @api.depends('barang_ids')
    def _compute_jml_item(self):
        for rec in self:
            a = self.env['sneakstore.barang'].search([('kelompokbarang_id','=', rec.id)]).mapped('name')
            b = len(a)
            rec.jml_item = b
            rec.daftar = a

    daftar = fields.Char(string='List')
    
    
    
