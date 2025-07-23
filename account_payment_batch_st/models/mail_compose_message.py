from odoo import models, fields, api
import base64
from odoo.tools import safe_eval


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _compute_attachment_ids(self):
        """ Extendemos el método original para que se pueda previsualizar en el envío de mails de lotes de pagos el/los archivos de retenciones. """
        super()._compute_attachment_ids()
        for composer in self:
            res_ids = composer._evaluate_res_ids() or [0]
            if composer.model == 'account.payment.batch.st' and composer.template_id and len(res_ids) == 1:
                batch = self.env[composer.model].browse(res_ids)
                if batch.partner_type != 'supplier':
                    return

                report = self.env.ref(
                    'l10n_ar_withholding_ux.action_report_withholding_certificate', 
                    raise_if_not_found=False)
                if not report:
                    return
                
                for withholding in batch.l10n_ar_withholding_ids:
                    report_name = safe_eval.safe_eval(report.print_report_name, {'object': withholding})
                    result, _ = self.env['ir.actions.report']._render(report.report_name, withholding.ids)
                    file = base64.b64encode(result)
                    data_attach = {
                        'name': report_name,
                        'datas': file,
                        'res_model': 'mail.compose.message',
                        'res_id': 0,
                        'type': 'binary',
                    }
                    composer.attachment_ids += self.env['ir.attachment'].create(data_attach)