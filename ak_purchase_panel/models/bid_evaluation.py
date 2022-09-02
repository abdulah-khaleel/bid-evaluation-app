 # -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError 


class BidEvaluation(models.Model):
    _inherit = 'bid.evaluation'

    bid_approver_ids = fields.Many2many('bid.panel.members', string="Panel Members")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], default='draft', string="Status", track_visibility=True)
    user_status = fields.Selection([
        ('pending', 'To Approve'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
        ], compute="_compute_user_status")
    edit_questions = fields.Selection([
        ('allowed', 'Allowed'),
        ('not_allowed', 'Not Allowed'),
        ], compute="_check_questions_edit_access")
    is_winning_bid = fields.Boolean('Winning Bid', copy=False) 
    winner_selection_complete = fields.Boolean('selection process complete', default=True)

    def create_activity(self):
        self.ensure_one()
        for member in self.bid_approver_ids.user_id:
                    self.activity_schedule('ak_purchase_panel.mail_bid_panel_member_evaluation_notification',
                        date_deadline=self.date or self.requisition_id.date_end, 
                        user_id = member.id, 
                        note=f"The Bid evaluation/scoring for the purchase agreement and vendor ref: {self.name} has been drafted by: {self.user_id.name} and is pending your review/approval.")
    
    def get_panel_member_activity(self,user):
        domain = [
            ('res_model', '=', 'bid.evaluation'),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', self.env.ref('ak_purchase_panel.mail_bid_panel_member_evaluation_notification').id),
            ('user_id', '=', user.id)
        ]
        activity = self.env['mail.activity'].search(domain,limit=1)
        return activity
     
    def submit_evaluation(self):
        self.ensure_one()
        for question in self.question_ids:
            if question.score == 0:
                raise ValidationError(
                    _(f"Scores should be between 1 and {self.score_limit}. Please make sure that all factors are scored properly and try again."))
        self.create_activity()
        self.write({'state': 'to_approve'})
        for approval in self.bid_approver_ids:
            approval.write({
                'review_state': 'pending'
                })

    def cancel_evaluation(self):
        domain = [
            ('res_model', '=', 'bid.evaluation'),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', self.env.ref('ak_purchase_panel.mail_bid_panel_member_evaluation_notification').id),
        ]
        activities = self.env['mail.activity'].search(domain)
        activities.sudo().unlink()
        self.write({'state': 'cancel'})
        for approval in self.bid_approver_ids:
            if approval.user_id.id == self.env.user.id:
                approval.write({
                    'review_state': 'cancel',
                    'approval_date': fields.Datetime.now(),
                    })
     
    def reset_to_draft(self):
        self.write({'state': 'draft'})
        # reset approval ids status to 'pending':
        self.bid_approver_ids.write({
            'review_state': 'pending',
            'approval_date': False
            })


    def approve_evaluation(self):
        for approver in self.bid_approver_ids:
            if approver.user_id.id == self.env.user.id:
                approver.write({
                    'review_state': 'approved',
                    'approval_date': fields.Datetime.now(),
                    })
                self.sudo().get_panel_member_activity(user=self.env.user).unlink()
                self.message_post(body='Evaluation reviewed and approved.')

            if not 'pending' in self.bid_approver_ids.mapped('review_state'):
                self.write({'state': 'done'})

    
    @api.depends('question_ids.name')
    def _check_questions_edit_access(self):
        for eval in self:
            if self.env.user.has_group('purchase.group_purchase_user'):
                eval.edit_questions = 'allowed'
            else:
                eval.edit_questions = 'not_allowed'
            # approval.user_status = approval.bid_approver_ids.filtered(lambda approver: approver.user_id == self.env.user).review_state

    @api.depends('bid_approver_ids.review_state')
    def _compute_user_status(self):
        for approval in self:
            approval.user_status = approval.bid_approver_ids.filtered(lambda approver: approver.user_id == self.env.user).review_state




class BidPanelMembers(models.Model):
    _name = 'bid.panel.members'
    _description = 'Bid Panel Members'

    bid_evaluation_id = fields.Many2one('bid.evaluation', string="Bid Evaluation")
    user_id = fields.Many2one('res.users', string="Panel Member", required=True)
    user_email = fields.Char('Email', related='user_id.login')
    review_state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
        ], default='pending', string="Review Status")
    approval_date = fields.Datetime('Approval Date', readonly=True)

 