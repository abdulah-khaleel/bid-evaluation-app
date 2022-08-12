# -*- coding: utf-8 -*-

from tabnanny import check
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    enable_panel = fields.Boolean('Enable Panel Committee', compute='_check_for_purchase_panel')
    eval_template_id = fields.Many2one('bid.evaluation.template', string="Bid Evaluation Template", ondelete="restrict")
    evaluation_guidelines = fields.Text('Evaluation Guidelines')
    selected_bid_id = fields.Many2one('purchase.order', string="Selected Bid", domain="[('requisition_id', '=', id)]")
    selection_justification = fields.Text('Justification/Notes')