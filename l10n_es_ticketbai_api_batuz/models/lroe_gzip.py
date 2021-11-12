# -*- coding: utf-8 -*-
# Copyright (2021) Binovo IT Human Project SL
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import gzip
import shutil
import base64
import os


class LROEGzip:

    @staticmethod
    def compress_lroe_xml_data(xml_data):
        if xml_data:
            compress_content = gzip.compress(base64.b64decode(xml_data))
            if compress_content:
                return str(len(compress_content)), compress_content
            else:
                return None, None
        else:
            return None, None

    @staticmethod
    def decompress_lroe_gzip_xml_data(gzip_xml_data):
        if gzip_xml_data:
            decompress_content = gzip.decompress(gzip_xml_data)
            if decompress_content:
                return str(len(decompress_content)), decompress_content
            else:
                return None, None
        else:
            return None, None

    @staticmethod
    def decompress_lroe_xml_f_in_data_out(xml_file_name_in):
        if xml_file_name_in:
            with gzip.open(xml_file_name_in, 'rb') as f_in:
                return f_in.read()

    @staticmethod
    def decompress_lroe_xml_f_in_f_out(xml_file_name_in, xml_file_name_out=None):
        if xml_file_name_in:
            with gzip.open(xml_file_name_in, 'rb') as f_in:
                xml_file_out = xml_file_name_out
                if not xml_file_name_out:
                    xml_file_out = os.path.splitext(
                        os.path.basename(xml_file_name_in))[0] + '.xml'
                with open(xml_file_out, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
