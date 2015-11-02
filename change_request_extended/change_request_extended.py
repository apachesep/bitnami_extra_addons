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

class res_partner(osv.Model):
    _inherit="res.partner"

#    def _find_child_name(self, cr, uid, ids, field_name, arg, context=None):
#        res = {}
#        print '\n function field of partner',field_name,ids,context
#        return res


    _columns={
        'street3':fields.char('street3',size=128),
        'minimum_order_value':fields.char('Minimum Order Value'),
        'ups_account_number':fields.char('UPS Account Number'),
        'fedex_account_number':fields.char('Fedex Account Number'),
        'quotation_ids': fields.one2many('sale.order', 'partner_id', 'Quatation', domain=[('state', '=', 'draft')]),
        'sale_order_line_ids': fields.one2many('sale.order', 'partner_id', 'Sale Order', domain=[('state', '!=', 'draft')]),
        'purchase_order_line_ids': fields.one2many('purchase.order', 'partner_id', 'Sale Order'),
        'customer_invoice_ids':fields.one2many('account.invoice','partner_id','Customer Invoice',domain=[('type','=','out_invoice')]),
        'supplier_invoice_ids':fields.one2many('account.invoice','partner_id','Supplier Invoice',domain=[('type','=','in_invoice')]),
#        'child_name_kanban': fields.function(_find_child_name, type="char", string="Contacts"),

    }

class crm_lead(osv.Model):
    _inherit="crm.lead"
    _columns={
        'part_number':fields.char('Part Number'),
        'quantity':fields.char('Quantity'),
        'target_price':fields.float('Target Price'),
        'questions_date':fields.date('Questions Date'),
        'need_by_date':fields.date('Need By Date'),
        'internal_part_number':fields.char('Internal Part Number'),
        'solicitation_number':fields.char('Solicitation Number'),
    }
class sale_order(osv.Model):
    _inherit = 'sale.order'
    _columns = {
        'minimum_order_value':fields.char('Minimum Order Value'),
        'ups_account_number':fields.char('UPS Account Number'),
        'fedex_account_number':fields.char('Fedex Account Number'),
        'customer_po':fields.char("Customer PO")
               }
    def onchange_partner_id(self, cr, uid ,ids, partner_id, context=None):
        if partner_id:
            res = super(sale_order,self).onchange_partner_id(cr, uid, ids, partner_id,context=context)
            partnre_read = self.pool.get('res.partner').read(cr,uid, partner_id,['minimum_order_value','ups_account_number','fedex_account_number'],context=context)
            res.get('value').update({
                                     'minimum_order_value':partnre_read.get('minimum_order_value'),
                                     'ups_account_number':partnre_read.get('ups_account_number'),
                                     'fedex_account_number':partnre_read.get('fedex_account_number'),
                                 })
            return res
        return {'value':{}}
class sale_order_line(osv.Model):
    _inherit="sale.order.line"
    _columns={
        'part_number':fields.char('Part Number'),
        'internal_part_number':fields.char('Internal Part Number'),
        'manufacturer':fields.many2one('res.partner','Manufacturer'),
        'condition':fields.selection([('factory_new','Factory New'),('new_surplus','New Surplus'),('overhauled','Overhauled'),('rebuilt','Rebuilt'),('repaired','Repaired'),('refurbished','Refurbished'),('as_is','As-Is')],'Condition'),
        'date_code':fields.char('Date Code'),
        'rohs':fields.char('RoHS'),
        'lead_time':fields.char('Lead Time' , required=True),
    }

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

class product_ul(osv.Model):
    _inherit = "product.ul"
    _description = "Shipping Unit"
    _columns = {
        'type' : fields.selection([('reel','Reel'),('ammo_pack','Ammo Pack'),('bulk', 'Bulk'), ('tube', 'Tube'),('tray','Tray'),('bag','Bag'),('box','Box'),('case','Case'),('unknown','Unknown')], 'Type', required=True),
    }

    _defaults = {
        'type': 'reel'
    }

class account_invoice(osv.Model):
    _inherit="account.invoice"
    _columns = {
        'customer_po':fields.char("Customer PO")
    }

    def custom_invoice_print(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'sent': True}, context=context)
        data = self.read(cr, uid, ids)[0]
        self_browse = self.browse(cr, uid, ids)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice2',
            'datas': datas,
            'name': 'Invoice ' + self_browse[0].number,
            'nodestroy' : True
        }

class account_invoice_line(osv.Model):
    _inherit="account.invoice.line"
    _columns={
        'internal_part_number':fields.char('Internal Part Number'),
        'part_number':fields.char('Part Number'),
    }

class account_payment_term(osv.Model):
    _inherit="account.payment.term"
    _columns={
        'discount':fields.float('Discount'),
    }

class purchase_order(osv.Model):
    _inherit = "purchase.order"
    
    STATE_SELECTION = [
        ('draft', 'Draft PO'),
        ('sent', 'RFQ'),
        ('confirmed', 'Waiting Approval'),
        ('approved', 'Purchase Confirmed'),
        ('except_picking', 'Shipping Exception'),
        ('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]
    

    def _quantity_sum(self, cr, uid, ids, field,arg, context=None):
        res = {}
        total = 0
        for record in self.browse(cr, uid, ids):
            total = 0
            for qty in record.order_line:
                total = total + qty.product_qty
            res[record.id] = total
        return res

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
        'quantity':fields.function(_quantity_sum, type='float', string='Quantity'),
        'anti_receipt_date':fields.date('Anticipated Receipt Date'),
        'lead_time':fields.char('Lead Time'),
        'produ':fields.function(_get_line_product,type = 'char',string='Products'),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True,
                                  help="The status of the purchase order or the quotation request. "
                                       "A request for quotation is a purchase order in a 'Draft' status. "
                                       "Then the order has to be confirmed by the user, the status switch "
                                       "to 'Confirmed'. Then the supplier must confirm the order to change "
                                       "the status to 'Approved'. When the purchase order is paid and "
                                       "received, the status becomes 'Done'. If a cancel action occurs in "
                                       "the invoice or in the receipt of goods, the status becomes "
                                       "in exception.",
                                  select=True, copy=False),
        
    }

class purchase_order_line(osv.Model):
    _inherit = "purchase.order.line"
    def _get_manfactures(self, cr, uid, ids, field_name,arg, context=None):
        res = {}
        res = {}.fromkeys(ids, 0.0)
        for partner_id in ids:
            child_ids = self.search(cr, uid, [('parent_id','=',partner_id)])
            child_name = ''
            for child_id in child_ids:
                child_name += self.browse(cr, uid, child_id, context=context).name + ','
            res.update({partner_id:child_name})
        return res
    _columns = {
        'part_number':fields.char('Part Number'),
        'internal_part_number':fields.char('Internal Part Number'),
        'manufacturer':fields.char('Manufacturer'),
        'condition':fields.selection([('factory_new','Factory New'),('new_surplus','New Surplus'),('overhauled','Overhauled'),('rebuilt','Rebuilt'),('repaired','Repaired'),('refurbished','Refurbished'),('as_is','As-Is')],'Condition'),
        'date_code':fields.char('Date Code'),
        'rohs':fields.char('RoHS'),
        'lead_time':fields.char('Lead Time'),
        'manfacturer_id':fields.related('product_id','manufacturer',type="many2one",relation="res.partner", string="Manufactures"),
        'quote_date':fields.related('order_id','date_order',type="datetime", relation='purchase.order',string="Quote Date"),
    }

class product_supplierinfo(osv.Model):
    _inherit = "product.supplierinfo"

    _columns = {
        'manufacturer':fields.char('Manufacturer'),
        'condition':fields.char('Condition'),
        'date_code':fields.date('Date Code'),
    }

class procurement_order(osv.osv):
    _inherit = 'procurement.order'


    def _get_po_line_values_from_proc(self, cr, uid, procurement, partner, company, schedule_date, context=None):
        if context is None:
            context = {}
        uom_obj = self.pool.get('product.uom')
        pricelist_obj = self.pool.get('product.pricelist')
        prod_obj = self.pool.get('product.product')
        acc_pos_obj = self.pool.get('account.fiscal.position')
        so_obj = self.pool.get('sale.order')
        seller_qty = procurement.product_id.seller_qty
        pricelist_id = partner.property_product_pricelist_purchase.id
        uom_id = procurement.product_id.uom_po_id.id
        qty = uom_obj._compute_qty(cr, uid, procurement.product_uom.id, procurement.product_qty, uom_id)
        if seller_qty:
            qty = max(qty, seller_qty)
        price = pricelist_obj.price_get(cr, uid, [pricelist_id], procurement.product_id.id, qty, partner.id, {'uom': uom_id})[pricelist_id]

        #Passing partner_id to context for purchase order line integrity of Line name
        new_context = context.copy()
        new_context.update({'lang': partner.lang, 'partner_id': partner.id})
        product = prod_obj.browse(cr, uid, procurement.product_id.id, context=new_context)
        taxes_ids = procurement.product_id.supplier_taxes_id
        #condition = procurement.condition
        #part_number = procurement.part_number
        taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)
        name = product.display_name
        so_name = procurement.group_id.name
        so_id = so_obj.search(cr,uid,[('name', '=', so_name)],context=context)
        print "\n\n======so_id=====",so_id
        if product.description_purchase:
            name += '\n' + product.description_purchase
        print "\n\n==========line_vals======",name,qty,procurement.product_id.id,uom_id
        if so_id:
            sale_order = so_obj.browse(cr, uid, so_id[0], context=new_context)
            for line in sale_order.order_line:
                part_number = line.part_number
                internal_part_number = line.internal_part_number
                manufacturer = line.manufacturer
                condition = line.condition
                date_code = line.date_code
                rohs = line.rohs
                lead_time = line.lead_time
                print "\n\n================sale_order_line========",part_number,internal_part_number,manufacturer,condition,date_code,rohs,lead_time
                return {
                    'name': name,
                    'product_qty': qty,
                    'product_id': procurement.product_id.id,
                    'product_uom': uom_id,
                    'price_unit': price or 0.0,
                    'date_planned': schedule_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'taxes_id': [(6, 0, taxes)],
                    'part_number':part_number,
                    'internal_part_number':internal_part_number,
                    'manufacturer':manufacturer,
                    'condition':condition,
                    'date_code':date_code,
                    'rohs':rohs,
                    'lead_time':lead_time,

                }
        else:
            return {
                'name': name,
                'product_qty': qty,
                'product_id': procurement.product_id.id,
                'product_uom': uom_id,
                'price_unit': price or 0.0,
                'date_planned': schedule_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'taxes_id': [(6, 0, taxes)],
            }


class product_supplierinfo(osv.osv):
    _inherit = "product.supplierinfo"

    _columns = {
                'min_ord_val':fields.float('Minimum Order Value'),
                }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
