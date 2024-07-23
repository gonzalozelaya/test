from odoo import models, fields, api

class MassPaymentWizard(models.TransientModel):
    _name = 'mass.payment.wizard'
    _description = 'Wizard to create a mass payment'

    payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money')], string='Payment Type', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    amount = fields.Float(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    payment_date = fields.Date(string='Payment Date', required=True, default=fields.Date.context_today)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method', required=True)
    mass_payment_id = fields.Many2one('mass.payment', string='Mass Payment')

    @api.multi
    def action_create_payment(self):
        self.ensure_one()
        Payment = self.env['account.payment']
        payment_vals = {
            'payment_type': self.payment_type,
            'partner_type': 'supplier' if self.payment_type == 'outbound' else 'customer',
            'partner_id': self.partner_id.id,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'payment_date': self.payment_date,
            'journal_id': self.journal_id.id,
            'payment_method_id': self.payment_method_id.id,
            'mass_payment_id': self.mass_payment_id.id,
        }
        payment = Payment.create(payment_vals)
        payment.post()
        return {'type': 'ir.actions.act_window_close'}