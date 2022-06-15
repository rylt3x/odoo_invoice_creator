import xlrd
import base64
import datetime
import os
from . import config


class ExcelParser:
    def __init__(self, binary):
        self.binary = binary

    # Build filename
    @staticmethod
    def _get_filename():
        filename = f'{datetime.datetime.now().timestamp()}.xlsx'
        return filename

    # Create excel file from bytes to make possible to open it
    def _get_file_from_binary(self):
        filename = self._get_filename()
        filepath = os.path.join(config.UPLOAD_DIR, filename)
        file = open(filepath, 'wb')
        file.write(base64.decodebytes(self.binary))
        file.close()
        self.filepath = filepath
        return filepath

    # Get dict from excel file
    @staticmethod
    def _parse_data(filepath: str) -> dict:
        xlrd_book = xlrd.open_workbook(filepath)
        sheet = xlrd_book.sheet_by_index(0)

        parsed_data = {}

        for row_number in range(sheet.nrows):
            sheet_rows = [val.value for val in sheet.row(row_number)]

            if row_number == 0:
                continue

            invoice_number = int(sheet_rows[0])
            invoice_date_due = xlrd.xldate.xldate_as_datetime(sheet_rows[1], datemode=xlrd_book.datemode)
            client_tag = str(sheet_rows[2])
            product_article = str(sheet_rows[3])
            quantity = int(sheet_rows[4])
            price_unit = int(sheet_rows[5])

            if client_tag not in parsed_data.keys():
                parsed_data[client_tag] = []

            parsed_data[client_tag].append({
                'name': invoice_number,
                'product_article': product_article,
                'invoice_date_due': invoice_date_due,
                'quantity': quantity,
                'price_unit': price_unit
            })

        return parsed_data

    def _delete_file(self):
        os.remove(self.filepath)

    @property
    def parsed_data(self):
        filepath = self._get_file_from_binary()
        parsed_data = self._parse_data(filepath)
        self._delete_file()
        return parsed_data


