# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    panel_id = fields.Many2one('purchase.panel', string="Purchase Committee", ondelete="restrict")


