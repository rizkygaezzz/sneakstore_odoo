from odoo import api, fields, models


class Barang(models.Model):
    _name = 'sneakstore.barang'
    _description = 'New Description'

    name = fields.Char(string='Sneakers Name')
    size = fields.Selection([
        ('43', '43'), 
        ('44', '44'), 
        ('45', '45'),
        ('46', '46'),
        ('47', '47')        
    ], string='Size')
    harga_jual = fields.Integer(string='Price',required=True)
    kelompokbarang_id = fields.Many2one(comodel_name='sneakstore.kelompokbarang', 
                                        string='Brand',
                                        ondelete='cascade')
    supplier_id = fields.Many2many(comodel_name='sneakstore.supplier', string='Supplier')
    stok = fields.Integer(string='Stock')