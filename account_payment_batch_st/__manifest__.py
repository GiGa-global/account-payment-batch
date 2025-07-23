# Copyright 2024 sumitec - Juan Pablo Garza <jgarza@sumitec.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Lote de pagos - Recibos y Ordenes de pago",
    "version": "17.0.2.1.0",
    "category": "Accounting",
    "website": "https://github.com/sumitec-odoo/account-addons",
    "author": "sumitec",
    "license": "AGPL-3",
    "depends":
        [
            "account", # core
            "account_payment_pro", # adhoc
            'l10n_ar_withholding_ux', # adhoc
            'l10n_ar_account_withholding', # adhoc
        ],
    "data":
        [
            "views/batch_receipt.xml",
            "views/account_payment_batch_st_views.xml",
            'views/mail_template_data.xml',
            "views/account_payment_views.xml",
            'security/ir.model.access.csv',
            "data/account_payment_batch_data.xml",
        ],
    "installable": True,
}
