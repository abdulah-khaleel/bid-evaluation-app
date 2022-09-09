# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    # enable_panel = fields.Boolean('Enable Panel Committee', compute='_check_for_purchase_panel')
    panel_id = fields.Many2one('purchase.panel', string="Purchase Committee", ondelete="restrict")


