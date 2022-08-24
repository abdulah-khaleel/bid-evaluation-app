# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PanelPanel(models.TransientModel):
    _name = 'panel.panel'

    name = fields.Char(string='Name', required=True) 
