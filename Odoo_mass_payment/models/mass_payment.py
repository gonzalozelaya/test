# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class MassPayment(models.Model):
    _name = 'mass.payment'
    _description = 'Mass Payment'

    name = fields.Char(string='Payment Reference', required=True)
    payment_date = fields.Date(string='Payment Date', required=True, default=fields.Date.context_today)
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money')], string='Payment Type', required=True)
    payment_ids = fields.One2many('account.payment', 'mass_payment_id', string='Payments')
    invoice_ids = fields.Many2many('account.move', string='Invoices', domain=[('move_type', 'in', ['out_invoice', 'in_invoice']), ('state', '=', 'posted'), ('invoice_payment_state', '!=', 'paid')])

    @api.multi
    def action_open_payment_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Payment',
            'res_model': 'mass.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mass_payment_id': self.id,
                'default_payment_type': self.payment_type,
                'default_payment_date': self.payment_date,
                'default_journal_id': self.journal_id.id,
                'default_payment_method_id': self.payment_method_id.id,
            }
        }

    @api.multi
    def action_process_payments(self):
        self.ensure_one()
        Payment = self.env['account.payment']
        total_amount = sum(self.invoice_ids.mapped('amount_residual'))
        if not self.invoice_ids:
            raise ValidationError("Please select at least one invoice to process payments.")

        for invoice in self.invoice_ids:
            payment_vals = {
                'payment_type': self.payment_type,
                'partner_type': 'supplier' if invoice.move_type == 'in_invoice' else 'customer',
                'partner_id': invoice.partner_id.id,
                'amount': invoice.amount_residual,
                'currency_id': invoice.currency_id.id,
                'payment_date': self.payment_date,
                'journal_id': self.journal_id.id,
                'payment_method_id': self.payment_method_id.id,
                'invoice_ids': [(6, 0, [invoice.id])],
                'mass_payment_id': self.id,
            }
            payment = Payment.create(payment_vals)
            payment.post()

        self._reconcile_payments()

    def _reconcile_payments(self):
        for payment in self.payment_ids:
            payment_reconcile_ids = payment.line_ids.filtered(lambda line: not line.reconciled)
            invoice_reconcile_ids = payment.invoice_ids.line_ids.filtered(lambda line: not line.reconciled)
            (payment_reconcile_ids + invoice_reconcile_ids).reconcile()
            

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    mass_payment_id = fields.Many2one('mass.payment', string='Mass Payment')