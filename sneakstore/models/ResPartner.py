from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'New Description'

    
    is_direksi = fields.Boolean(string='Is Direksi')
    is_konsumen = fields.Boolean(string='Is Konsumen')
    poin = fields.Integer(string='Poin', domain="[('is_konsumen', '=', True)]")
    level = fields.Char(string='Level')