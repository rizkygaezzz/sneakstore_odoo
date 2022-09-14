from odoo import api, fields, models


class BarangDatang(models.TransientModel):
    _name = 'sneakstore.barangdatang'

    barang_id = fields.Many2one(
        comodel_name='sneakstore.barang',
        string='Sneakers Name',
        required=True)


    jumlah = fields.Integer(
        string='Total',
        required=False)

    def button_barang_datang(self):
        for rec in self:
            self.env['sneakstore.barang'] \
                .search([('id', '=', rec.barang_id.id)]) \
                .write({'stok': rec.barang_id.stok + rec.jumlah})