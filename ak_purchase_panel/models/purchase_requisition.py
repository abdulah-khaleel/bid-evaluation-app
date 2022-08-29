# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    # enable_panel = fields.Boolean('Enable Panel Committee', compute='_check_for_purchase_panel')
    panel_id = fields.Many2one('purchase.panel', string="Purchase Committee", ondelete="restrict")

    # def action_open(self):
    #     if self.type_id.enable_evaluation:
    #         if self.panel_id:
    #             for user in self.panel_id.member_ids:
    #                 self.activity_schedule('ak_purchase_agreement_panel.mail_purchase_panel_member_notification',
    #                     date_deadline=self.date_end, 
    #                     user_id = user.id, 
    #                     note=f"""The bid evaluation process for the purchase agreement: {self.name} has started. As part of the purchase committee, you will soon be notified
    #                     once evaluations for individual bids starts.""") 
    #         # else:
    #         #     raise ValidationError(_('You need to select a Purchase Committee before validating this agreement.'))
    #     return super(PurchaseRequisition,self).action_open()


