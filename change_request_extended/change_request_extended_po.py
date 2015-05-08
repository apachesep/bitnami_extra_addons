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

from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class sale_order(osv.Model):
    _inherit = 'sale.order'
    _columns = {
        'customer_po':fields.char("Customer PO")
    }

class purchase_order(osv.Model):
    _inherit = "purchase.order"
    def _get_line_product(self, cr, uid, ids, field,arg, context=None):
        res = {}
        res = {}.fromkeys(ids, 0.0)
        for record_ids in self.browse(cr, uid, ids):
            produ=''
            for orderline_id in record_ids.order_line:
                produ += orderline_id.product_id.name +','
                res[record_ids.id] = produ
        return res

    _columns = {
        'produ':fields.function(_get_line_product,type = 'char',string='Products'),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
