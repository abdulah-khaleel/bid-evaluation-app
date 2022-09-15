# -*- coding: utf-8 -*-

from odoo import models, fields, _


class PurchasePanel(models.Model):
    _name = 'purchase.panel'
    _description = 'Purchase Panel'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string="Panel Title", required=True)
    member_ids = fields.Many2many('res.users', string="Panel Members")
