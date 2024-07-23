from odoo import models, fields, api, Command, _
from odoo.exceptions import ValidationError, UserError

class MultiPayment(models.Model):
    _inherit = 'account.payment'
    
    _name = 'multi.payment'
    
    _description = 'Multiple Payment'

    date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True)
    payment_line_ids = fields.Many2many(
        'account.move.line',
        'account_move_line_payment_to_pay_rel',
        'multi_payment_id',
        'to_pay_line_id',
        string="To Pay Lines",
        compute='_compute_to_pay_move_lines', store=True,
        help='This lines are the ones the user has selected to be paid.',
        copy=False,
        readonly=False,
        check_company=True,
    )
    
    @api.depends('partner_id', 'partner_type', 'company_id')
    def _compute_to_pay_move_lines(self):
        # TODO ?
        # # if payment group is being created from a payment we dont want to compute to_pay_move_lines
        # if self._context.get('created_automatically'):
        #     return

        # Se recomputan las lienas solo si la deuda que esta seleccionada solo si
        # cambio el partner, compania o partner_type
        for rec in self:
            if rec.partner_id != rec._origin.partner_id or rec.partner_type != rec._origin.partner_type or \
                    rec.company_id != rec._origin.company_id:
                rec.add_all()

    def _get_to_pay_move_lines_domain(self):
        self.ensure_one()
        return [
            ('partner_id.commercial_partner_id', '=', self.partner_id.commercial_partner_id.id),
            ('company_id', '=', self.company_id.id), ('move_id.state', '=', 'posted'),
            ('account_id.reconcile', '=', True), ('reconciled', '=', False), ('full_reconcile_id', '=', False),
            ('account_id.account_type', '=', 'asset_receivable' if self.partner_type == 'customer' else 'liability_payable'),
        ]

    def add_all(self):
        for rec in self:
            rec.to_pay_move_line_ids = [Command.clear(), Command.set(self.env['account.move.line'].search(rec._get_to_pay_move_lines_domain()).ids)]

    def remove_all(self):
        self.to_pay_move_line_ids = False

#class MultiPaymentLine(models.Model):
 #   _name = 'multi.payment.line'
 #   _description = 'Multiple Payment Line'
#
 #   multi_payment_id = fields.Many2one('multi.payment', string='Multi Payment Reference', required=True, ondelete='cascade')
  #  move_line_id = fields.Many2one('account.move.line', string='Journal Item', required=True)
   # amount_due = fields.Monetary(string='Amount Due', related='move_line_id.balance', currency_field='company_currency_id')
    #amount_paid = fields.Monetary(string='Amount Paid', currency_field='company_currency_id')
    #company_currency_id = fields.Many2one('res.currency', string='Currency', related='multi_payment_id.journal_id.currency_id', readonly=True)