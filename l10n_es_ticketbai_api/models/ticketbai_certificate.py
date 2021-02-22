# Copyright 2017 Diagram Software S.L.
# Copyright 2021 Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import os
import base64
import contextlib
import tempfile
import logging
from odoo.tools import config
from odoo import models, fields, api, release

_logger = logging.getLogger(__name__)

try:
    from OpenSSL import crypto
except(ImportError, IOError) as err:
    _logger.error(err)


@contextlib.contextmanager
def pfx_to_pem(file, pfx_password, directory=None):
    with tempfile.NamedTemporaryFile(
            prefix='private_', suffix='.pem', delete=False,
            dir=directory) as t_pem:
        f_pem = open(t_pem.name, 'wb')
        p12 = crypto.load_pkcs12(file, pfx_password)
        f_pem.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))
        f_pem.close()
        yield t_pem.name


@contextlib.contextmanager
def pfx_to_crt(file, pfx_password, directory=None):
    with tempfile.NamedTemporaryFile(
            prefix='public_', suffix='.crt', delete=False,
            dir=directory) as t_crt:
        f_crt = open(t_crt.name, 'wb')
        p12 = crypto.load_pkcs12(file, pfx_password)
        f_crt.write(crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))
        f_crt.close()
        yield t_crt.name


class TicketBaiCertificate(models.Model):
    _name = 'tbai.certificate'
    _description = 'TicketBAI Certificate for signing the XML files'

    name = fields.Char(required=True)
    company_id = fields.Many2one(
        string='Company', comodel_name='res.company', required=True,
        default=lambda self: self.env.user.company_id.id)
    datas = fields.Binary('P12 Certificate', required=True)
    password = fields.Char(default='')
    public_key = fields.Char(
        string="Public Key", compute='_compute_p12', store=True, readonly=True)
    private_key = fields.Char(
        string="Private Key", compute='_compute_p12', store=True, readonly=True)

    @api.multi
    @api.depends('datas', 'password')
    def _compute_p12(self):
        directory = os.path.join(
            os.path.abspath(config['data_dir']), 'certificates',
            release.series, self.env.cr.dbname, 'l10n_es_ticketbai_api')
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        for record in self:
            file = base64.decodebytes(record.datas)
            with pfx_to_pem(file, self.password, directory) as private_key:
                record.private_key = private_key
            with pfx_to_crt(file, self.password, directory) as public_key:
                record.public_key = public_key

    def get_p12(self):
        """
        :return: OpenSSL.crypto.PKCS12
        """
        self.ensure_one()
        with open(self.public_key, 'rb') as f_crt:
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, f_crt.read())
        p12 = crypto.PKCS12()
        p12.set_certificate(cert)
        with open(self.private_key, 'rb') as f_pem:
            private_key = f_pem.read()
        p12.set_privatekey(crypto.load_privatekey(crypto.FILETYPE_PEM, private_key))
        return p12
