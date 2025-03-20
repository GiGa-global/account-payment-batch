# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,  api, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    abs_amount_currency = fields.Monetary(string='Importe', compute='_compute_abs_amount_currency', store=True)


    @api.depends('amount_currency')
    def _compute_abs_amount_currency(self):
        for line in self:
            line.abs_amount_currency = abs(line.amount_currency)
