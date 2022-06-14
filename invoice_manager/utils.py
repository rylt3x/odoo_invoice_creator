import odoo
from .excel_parser import ExcelParser


def _get_parsed_data(binary: bytes) -> dict:
    parser = ExcelParser(binary)
    parsed_data = parser.parsed_data
    return parsed_data


def _get_customer_by_tag(self, tag:str) -> int:
    customers = self.env['res.partner'].search([('category_id', '=', tag)])
    customer_id = customers[0].id
    return customer_id


def _get_product_by_article(self, article: str) -> int:
    product_id = self.env['product.product'].search([('default_code', '=', article)])
    product_id = product_id[0].id
    return product_id


def create_invoice(self, file_bytes):
    invoice_data = _get_parsed_data(file_bytes)

    for tag, lines in invoice_data.items():
        partner_id = _get_customer_by_tag(self, tag)
        invoice_date_due = ''
        invoice_name = ''
        product_id = ''
        line_data = []
        for line in lines:
            invoice_date_due = line.pop('invoice_date_due')
            invoice_name = line.pop('name')
            product_id = _get_product_by_article(self, line.pop('product_article'))
            line['product_id'] = product_id
            line_data.append(line)

        invoice_vals = {
            'name': invoice_name,
            'partner_id': partner_id,
            'invoice_date': invoice_date_due,
            'move_type': 'out_invoice',
            'journal_id': 1,
            'invoice_line_ids': line_data
        }
        self.env['account.move'].create(invoice_vals)

    return invoice_data





