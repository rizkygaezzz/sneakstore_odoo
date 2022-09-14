from odoo import api, fields, models


class Supplier(models.Model):
    _name = 'sneakstore.supplier'
    _description = 'New Description'

    name = fields.Char(string='Company')
    alamat = fields.Char(string='Address')
    no_telp = fields.Char(string='Number')
    barang_id = fields.Many2many(comodel_name='sneakstore.barang', string='Sneakers')