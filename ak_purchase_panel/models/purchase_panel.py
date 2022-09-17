# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PurchasePanel(models.Model):
    _name = 'purchase.panel'
    _description = 'Purchase Panel'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string="Panel Title", required=True)
    member_ids = fields.Many2many('res.users', string="Panel Members")

    @api.constrains('member_ids')
    def _check_panel_members(self):
        if len(self.member_ids) < 1:
            raise ValidationError(_('You must add at least one panel member.'))
