# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..invoice_manager import create_invoice
from ..invoice_manager import config


class Attachment(models.Model):
    _name = 'invoice_mgr.attachment'
    _description = 'Модель загруженного файла'
    file_name = fields.Char(string='File name')
    file_path = fields.Binary(string='Attached file')

    @api.model
    def create(self, vals):
        file_name = vals.get('file_name', '')
        file_extension = self._get_file_extension(file_name)
        if not self._is_extension_supported(file_extension):
            raise TypeError('File extension not supported')
        return super(Attachment, self).create(vals)

    @staticmethod
    def _is_extension_supported(file_extension: str) -> bool:
        available_extensions = ['xlsx', 'xls']
        if file_extension not in available_extensions:
            return False
        return True

    @staticmethod
    def _get_file_extension(file_name: str) -> str:
        return file_name.split('.')[-1]

    def create_invoice(self):
        for s in self:
            # print(config.UPLOAD_DIR)
            create_invoice(s, s.file_path)
        return
