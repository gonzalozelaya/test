from odoo import models, fields, api

class MultiPayment(models.Model):
    _name = 'multi.payment'
    _description = 'Multiple Payment'

    date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    payment_line_ids = fields.One2many('multi.payment.line', 'multi_payment_id', string='Pending Balances')

class MultiPaymentLine(models.Model):
    _name = 'multi.payment.line'
    _description = 'Multiple Payment Line'

    multi_payment_id = fields.Many2one('multi.payment', string='Multi Payment Reference', required=True, ondelete='cascade')
    move_line_id = fields.Many2one('account.move.line', string='Journal Item', required=True)
    amount_due = fields.Monetary(string='Amount Due', related='move_line_id.amount_residual', currency_field='company_currency_id')
    amount_paid = fields.Monetary(string='Amount Paid', currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', string='Currency', related='multi_payment_id.journal_id.currency_id', readonly=True)