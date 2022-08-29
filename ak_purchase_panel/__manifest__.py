# -*- coding: utf-8 -*-
################################################################################# 
#
#    Author: Abdullah Khalil. Copyrights (C) 2022-TODAY reserved. 
#
#    You may use this app as per the rules outlined in the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3. 
#    See <http://www.gnu.org/licenses/> for more detials.
#
################################################################################# 

{
    'name': "Purchase Panels",   
    'summary': "Enable purchase panels to participate in bids evaluation",   
    'description': """
        This app extends the bids evaluation app by enabling purchase panels to participate in evaluating
        bids/quotations for a given tender/purchase agreement. The app allows creation of panels or
        comittees, and a validation workflow for approving each evaluation. The app also extends bid evaluation 
        reports by adding purchase panel details into them.
    """,   
    'author': "Abdullah Khalil",
    'website': "https://github.com/abdulah-khaleel",
    'category': 'Purchase',
    'version': '14.0.0.0',
     "license": "LGPL-3",
    'depends': ['ak_bid_evaluation'],
    'data': [
        'security/purchase_panel_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_panel_views.xml',
        'views/purchase_requisition_views.xml',
        'views/bid_evaluation_views.xml',
    ],
    # 'images': ["static/description/banner-v15.png"],
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
} 
