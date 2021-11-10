# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common
from .common import TestL10nEsTicketBAIAPI


@common.at_install(False)
@common.post_install(True)
class TestL10nEsTicketBAIInvoice(TestL10nEsTicketBAIAPI):

    def test_send_pending_invoices_never_raises(self):
        def raise_exception():
            raise Exception("Raised on test_send_pending_invoices_never_raises")
        Invoice = self.env['tbai.invoice']
        Invoice.send_pending_invoices_impl = raise_exception
        Invoice.send_pending_invoices()
