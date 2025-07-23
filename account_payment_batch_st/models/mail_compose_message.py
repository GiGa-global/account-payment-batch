from odoo import models, fields, api
import base64
from odoo.tools import safe_eval
from odoo.exceptions import MissingError
import logging

_logger = logging.getLogger(__name__)


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
                
                # Obtener todas las retenciones de los pagos del lote
                all_withholdings = self.env['l10n_ar.payment.withholding']
                for payment in batch.payment_ids:
                    if hasattr(payment, 'l10n_ar_withholding_line_ids'):
                        for withholding in payment.l10n_ar_withholding_line_ids:
                            try:
                                # Verificar que el registro existe
                                if withholding.exists():
                                    all_withholdings |= withholding
                            except MissingError:
                                _logger.warning(f"Withholding record {withholding.id} no longer exists, skipping")
                                continue
                            except Exception as e:
                                _logger.warning(f"Error checking withholding record {withholding.id}: {e}")
                                continue
                
                for withholding in all_withholdings:
                    try:
                        if not withholding.exists():
                            continue
                            
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
                    except MissingError:
                        _logger.warning(f"Withholding record {withholding.id} no longer exists, skipping")
                        continue
                    except Exception as e:
                        _logger.error(f"Error generating withholding certificate for {withholding.id}: {e}")
                        continue