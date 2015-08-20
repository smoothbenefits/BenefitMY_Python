from pdf_tk_engine import get_template


class PDFFormFillService(object):

    def fill_form(self, template_name, field_map, http_response):
        template = get_template(template_name)
        http_response.write(template.render(field_map))
