# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_panel_members(self):
        members_list = []
        for member in self.requisition_id.panel_id.member_ids:
            members_list.append((0, 0, {'user_id': member.id, 'review_state': 'pending'}))
        return members_list


    def create_bid_evaluation(self):
        if not self.requisition_id.eval_template_id:
            raise UserError(_("You have not specified a a bid evaluation template on the requisition record. Please set the evaluation template and retry."))
        if self.env['bid.evaluation'].search([('purchase_order_id', '=', self.id)]):
            self.write({'has_evaluation': True})
            return self.get_bid_evaluation_record()
        else:
            bid_evaluation_record = self.env['bid.evaluation'].sudo().create({
                'name': f'Bid Evaluation - {self.requisition_id.name} - {self.partner_id.name}',
                'purchase_order_id': self.id,
                'requisition_id': self.requisition_id.id,
                'partner_id': self.partner_id.id,
                # user_id equals to current logged in user:
                'user_id': self.env.user.id,
                'date': fields.Date.today(),
                'evaluation_guidelines': self.requisition_id.evaluation_guidelines,
                'score_limit': self.requisition_id.eval_template_id.score_limit,
                'checklist_item_ids': self.get_checklist_item_ids(),
                'question_ids': self.get_question_ids(),
                'bid_approver_ids': self.get_panel_members() 
            })
            # bid_evaluation_record.sudo().write({
            # 'bid_approver_ids': self.get_panel_members() 
            # })
            self.write({'has_evaluation': True})
            return self.get_bid_evaluation_record()

   