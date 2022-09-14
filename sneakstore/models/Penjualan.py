from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Penjualan(models.Model):
    _name = 'sneakstore.penjualan'
    _description = 'New Description'

    name = fields.Char(string='Bill Number')
    nama_pembeli = fields.Char(string='Buyer')
    tgl_penjualan = fields.Datetime(string='Date', default = fields.Datetime.now())
    total_bayar = fields.Integer(compute='_compute_totalbayar', string='Total Price')
    detailpenjualan_ids = fields.One2many(
        comodel_name='sneakstore.detailpenjualan', 
        inverse_name='penjualan_id', 
        string='Details')   

    @api.depends('detailpenjualan_ids')
    def _compute_totalbayar(self):
        for rec in self:
            a = sum(self.env['sneakstore.detailpenjualan'].search([('penjualan_id','=',rec.id)]).mapped('subtotal'))
            rec.total_bayar = a

    # @api.ondelete(at_uninstall=False)
    # def __ondelete_penjualan(self):
    #     if self.detailpenjualan_ids:
    #         a=[]
    #         for rec in self:
    #             a = self.env['sneakstore.detailpenjualan'].search([('penjualan_id','=',rec.id)])
    #             print(a)
    #         for ob in a:
    #             print(str(ob.barang_id.name) + ' ' + str(ob.qty))
    #             ob.barang_id.stok += ob.qty

    def unlink(self):
        if self.detailpenjualan_ids:
            a=[]
            for rec in self:
                a = self.env['sneakstore.detailpenjualan'].search([('penjualan_id','=',rec.id)])
                print(a)
            for ob in a:
                print(str(ob.barang_id.name) + ' ' + str(ob.qty))
                ob.barang_id.stok += ob.qty
        record = super(Penjualan,self).unlink()

    def write(self,vals):
        for rec in self:
            a = self.env['sneakstore.detailpenjualan'].search([('penjualan_id','=',rec.id)])
            print(a)
            for data in a:
                print(str(data.barang_id.name)+' '+str(data.qty)+' '+str(data.barang_id.stok))
                data.barang_id.stok += data.qty
        record = super(Penjualan,self).write(vals)
        for rec in self:
            b = self.env['sneakstore.detailpenjualan'].search([('penjualan_id','=',rec.id)])
            print(a)
            print(b)
            for databaru in b:
                if databaru in a:
                    print(str(databaru.barang_id.name)+' '+str(databaru.qty)+' '+str(databaru.barang_id.stok))
                    databaru.barang_id.stok -= databaru.qty
                else:
                    pass
        return record

    _sql_constraints = [
        ('no_nota_unik','unique (name)','Bill Number Already Exist')
    ]



class DetailPenjualan(models.Model):
    _name = 'sneakstore.detailpenjualan'
    _description = 'New Description'

    name = fields.Char(string='Name')
    penjualan_id = fields.Many2one(comodel_name='sneakstore.penjualan', string='Details')
    barang_id = fields.Many2one(comodel_name='sneakstore.barang', string='Sneakers List')
    harga_satuan = fields.Integer(string='Price per Piece')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')
    
    @api.depends('harga_satuan','qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.harga_satuan
    
    @api.onchange('barang_id')
    def _onchange_barang_id(self):
        if (self.barang_id.harga_jual):
            self.harga_satuan = self.barang_id.harga_jual
    
    @api.model
    def create(self,vals):
        record = super(DetailPenjualan,self).create(vals)
        if record.qty:
            self.env['sneakstore.barang'].search([('id','=',record.barang_id.id)]).write({'stok' : record.barang_id.stok - record.qty})
        return record

    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            if rec.qty <1:
                raise ValidationError("Minimum {} Is 1".format(rec.barang_id.name))
            elif (rec.barang_id.stok < rec.qty):
                raise ValidationError('Stock For {} Is Not Sufficient, Only {} Left'.format(rec.barang_id.name,rec.barang_id.stok))
    
    