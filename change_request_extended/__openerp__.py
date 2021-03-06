# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2013-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Change Request Extended for Customer PO',
    'version': '1.0',
    'category': 'Sale',
    'description': """
    """,
    'author': 'BrowseInfo',
    'website': 'http://browseinfo.in',
    'depends': ['sale', 'purchase', 'crm', 'product', 'account', 'sale_stock', 'sale_invoice_discount'],
    'data': [
        'change_request_extended_view.xml',
        'change_request_extended_data.xml',
        'report_view.xml',
        'views/report_invoice.xml',
        'views/report_purchaseorder.xml',
        'views/report_saleorder.xml',
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
