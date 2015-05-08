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

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=partner_id,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=context)
        if res.get('value'):
            if res.get('value').get('price_unit'):
                del res['value']['price_unit']
        return res

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        """Prepare the dict of values to create the new invoice line for a
           sales order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: sale.order.line record to invoice
           :param int account_id: optional ID of a G/L account to force
               (this is used for returning products including service)
           :return: dict of values to create() the invoice line
        """
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=account_id, context=context)
        
        res.update({'part_number': line.part_number, 'internal_part_number' : line.internal_part_number})
        return res


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
