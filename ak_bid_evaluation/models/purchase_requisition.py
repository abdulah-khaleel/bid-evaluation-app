# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    enable_evaluation = fields.Boolean('Enable Evaluation', compute='_check_for_evaluation')
    eval_template_id = fields.Many2one('bid.evaluation.template', string="Bid Evaluation Template", ondelete="restrict", 
                                help="""Choose the evaluation template that you would like to use for this agreement. 
                                        You can edit questions on individual evaluation records if needed.""")
    evaluation_guidelines = fields.Text('Evaluation Guidelines', help="Guidelines noted here will also be listed on each bid evaluation record.")
    selected_bid_ids = fields.Many2many('purchase.order', string="Selected Bids", domain="[('requisition_id', '=', id)]",
                                help="Confirmed quotations will automatically be added to this list. However, you can still add quotations manually if required.")
    selection_justification = fields.Text('Justification/Notes', help="Any remarks relevant to the bid selection and evaluation process.")

    def get_checklist_summary_titles(self):
        """Function used in the 'Bids Checklist Summary' report to print the first row of the checklist table"""
        evaluation_records = self.env['bid.evaluation'].search([('requisition_id', '=', self.id),('state', 'in', ['done','to_approve','draft'])])
        return sorted(list(set(evaluation_records.mapped('checklist_item_ids.name'))))

    def get_checklist_summary_lines(self):
        """Function used in the 'Bids Checklist Summary' report to print the checklist status for each of the bids of an agreement"""
        evaluation_records = self.env['bid.evaluation'].search([('requisition_id', '=', self.id),('state', '=', ['done','to_approve', 'draft'])])
        checklist_item_names = sorted(list(set(evaluation_records.mapped('checklist_item_ids.name'))))
        
        checklist_l = []
        for rec in evaluation_records:
            bidder_list = []
            bidder_list.append(rec.partner_id.name)
            bidder_list.append(rec.purchase_order_id.name)
            partner_dict = {}
            if len(rec.checklist_item_ids) == 0:
                for name in checklist_item_names:
                    partner_dict[name] = 'N/A' 
            else:
                for checklist_title in checklist_item_names:
                    for line in rec.checklist_item_ids:
                        if line.name == checklist_title:
                            partner_dict[line.name] = line.item_clear
            for title in checklist_item_names:
                if title not in partner_dict:
                    partner_dict[title] = 'N/A'

            # sorted_partner_dict = {}
            sorted_partner_dict = {key: value for key, value in sorted(partner_dict.items())}

            bidder_list.append(sorted_partner_dict)
            checklist_l.append(bidder_list)
        return checklist_l

    def get_evaluation_questions(self):
        """Function used in the Evaluation Summary report to generate the first row for the evaluation scoring table."""
        evaluation_records = self.env['bid.evaluation'].search([('requisition_id', '=', self.id),('state', 'in', ['done','to_approve', 'draft'])])
        question_titles = sorted(list(set(evaluation_records.mapped('question_ids.name'))))
        question_titles.append('Average Score')
        return question_titles

    def get_evaluation_summary_lines(self):
        """Function used in the Evaluation Summary report to generate the data for the evaluation scoring table."""
        evaluation_records = self.env['bid.evaluation'].search([('requisition_id', '=', self.id),('state', 'in', ['done','to_approve', 'draft'])])
        question_titles = sorted(list(set(evaluation_records.mapped('question_ids.name'))))
        
        eval_list = []
        for rec in evaluation_records:
            bidder_list = []
            bidder_list.append(rec.partner_id.name)
            bidder_list.append(rec.purchase_order_id.name)
            partner_dict = {}
            if len(rec.question_ids) == 0:
                for name in question_titles:
                    partner_dict[name] = ' - '
            else:
                for question in question_titles:
                    for line in rec.question_ids:
                        if line.name == question:
                            partner_dict[line.name] = line.score
            for title in question_titles:
                if title not in partner_dict:
                    partner_dict[title] = ' - '

            # sorted_partner_dict = {}
            sorted_partner_dict = {key: value for key, value in sorted(partner_dict.items())}
            sorted_partner_dict['Average Score'] = round(rec.score_avg,2)
            bidder_list.append(sorted_partner_dict)
            eval_list.append(bidder_list)

        return eval_list

    def get_agreement_lines(self):
        """Function used in the comparative bids report to list down the purchase agreement lines"""
        # agreement_lines structure = [['Item A',3.0],['Item B', 4.0],['Item C', 10.0]]
        agreement_lines = []
        for line in self.line_ids.sorted(key=lambda r: r.product_id.id):
            agreement_lines.append([line.product_id.name, line.product_qty])
        return agreement_lines

    def get_agreement_quotations(self):
        """Function used in the comparative bids report to list down quotation details (prices and quantities) for each of the bids"""
        # Structure of the list of prices:
        # [
            # ['Vendor Name', 'PO3111', {
            #     product_id: [Unit Price, Subtotal],
            #     product_id: [Unit Price, Subtotal],
            #     }, 
            # Total Quote Price]
        # ]
      
        # unsorted_quotation_ids = self.env['purchase.order'].search([('requisition_id', '=', self.id)])
        quotation_ids = self.env['purchase.order'].search([('requisition_id', '=', self.id)]).sorted(key=lambda r: r.amount_total)
        product_ids = list(set(self.line_ids.mapped('product_id.id')))

        quotations_list = []
        for quotation in quotation_ids:
            vendor_list = []
            vendor_list.append(quotation.name)
            vendor_list.append(quotation.partner_id.name)
            vendor_dict = {}
            if len(quotation.order_line) == 0:
                for product_id in product_ids:
                    vendor_dict[product_id] = ['-','-']
            else:
                for product_id in product_ids:
                    for line in quotation.order_line:
                        if line.product_id.id == product_id:
                            vendor_dict[line.product_id.id] = [line.currency_id.symbol + ' ' + str(line.price_unit), line.currency_id.symbol + ' ' + str(line.price_subtotal)]
            for product_id in product_ids:
                if product_id not in vendor_dict:
                    vendor_dict[product_id] = ['-','-']

            sorted_vendor_dict = {key: value for key, value in sorted(vendor_dict.items())}
            vendor_list.append(sorted_vendor_dict)
            vendor_list.append(quotation.currency_id.symbol + ' ' + str(quotation.amount_total))
            quotations_list.append(vendor_list)
        return quotations_list

    # def check_number_of_lines(self):
    #     if len(self.line_ids) > 5:
    #         raise UserError(_("Cannot generate a comparative report for more than 5 lines."))
    #     return True
     
    @api.depends('type_id')
    def _check_for_evaluation(self):
        if self.type_id.enable_evaluation:
            self.sudo().write({'enable_evaluation': True})
        else:
            self.sudo().write({'enable_evaluation': False})
     