from odoo.tests import tagged

from .test_edi_common import TestL10nECEdiCommon


@tagged("post_install", "-at_install")
class TestAccountEdiFormat(TestL10nECEdiCommon):
    def test_is_required_for_invoice(self):
        """Verificar si se requiere edi_format en las facturas
        y si es compatible con el diario"""
        invoice = self._l10n_ec_create_in_invoice()
        self.assertFalse(self.edi_format._get_move_applicability(invoice))
        # Cambiar los datos de la factura
        invoice.company_id.country_id = self.env.ref("base.co")
        invoice.journal_id.type = "sale"
        invoice.move_type = "out_invoice"
        self.assertTrue(self.edi_format._get_move_applicability(invoice))
        # Comprobar si el edi_format es compatible con el diario
        self.assertTrue(self.edi_format._is_compatible_with_journal(invoice.journal_id))
