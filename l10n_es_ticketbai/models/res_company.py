# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    tbai_aeat_certificate_id = fields.Many2one(
        comodel_name='l10n.es.aeat.certificate', string='AEAT Certificate',
        domain="[('state', '=', 'active'), ('company_id', '=', id)]", copy=False)

    @api.onchange('tbai_enabled')
    def onchange_tbai_enabled_unset_tbai_aeat_certificate_id(self):
        if not self.tbai_enabled:
            self.tbai_aeat_certificate_id = False

    def tbai_certificate_get_p12(self):
        if self.tbai_aeat_certificate_id:
            cert = self.tbai_aeat_certificate_id.get_p12()
        else:
            cert = super().tbai_certificate_get_p12()
        return cert

    def tbai_certificate_get_public_key(self):
        if self.tbai_aeat_certificate_id:
            public_key = self.tbai_aeat_certificate_id.public_key
        else:
            public_key = super().tbai_certificate_get_public_key()
        return public_key

    def tbai_certificate_get_private_key(self):
        if self.tbai_aeat_certificate_id:
            private_key = self.tbai_aeat_certificate_id.private_key
        else:
            private_key = super().tbai_certificate_get_private_key()
        return private_key
