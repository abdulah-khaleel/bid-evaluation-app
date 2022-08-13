# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    has_evaluation = fields.Boolean(string='Has Evaluation', default=False, copy=False)
    evaluation_count = fields.Integer(compute="_compute_evaluations_count")

    def get_bid_evaluation_record(self):
        self.ensure_one()
        bid_evaluation_record = self.env['bid.evaluation'].search([('po_id', '=', self.id)])
        if bid_evaluation_record:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Bid Evaluation',
                'view_mode': 'form',
                'res_model': 'bid.evaluation',
                'res_id': bid_evaluation_record.id,
                'domain': [('po_id', '=', self.id)],
            }
    
    def create_bid_evaluation(self):
        if not self.requisition_id.eval_template_id:
            raise UserError(_("You have not specified a a bid evaluation template on the requisition record. Please set the evaluation templateand retry."))
        return True
        # bid_evaluation_record = self.env['bid.evaluation'].sudo().create({
        #     'name': f'Bid Evaluation - {self.requisition_id.name} - {self.partner_id.name}',
        #     'po_id': self.id,
        #     'purchase_requisition_id': self.requisition_id.id,
        #     'partner_id': self.partner_id.id,
        #     'deadline': self.date_order,
        #     'evaluation_guidelines': self.requisition_id.evaluation_guidelines,
        #     'score_limit': self.requisition_id.eval_template_id.score_limit,
        #     'checklist_item_ids': self.get_checklist_item_ids(),
        #     'question_ids': self.get_question_ids()
        #   })
        # # bid_evaluation_record = self.env['bid.evaluation'].search([('po_id', '=', self.id)])
        # bid_evaluation_record.sudo().write({
        #     'bid_approver_ids': self.get_panel_members()
        # })
        # self.write({'has_evaluation': True})
        # return self.get_bid_evaluation_record()
    
    def _compute_evaluations_count(self):
        BidEvaluations = self.env['bid.evaluation']
        self.evaluation_count = BidEvaluations.search_count([('po_id', '=', self.id)])