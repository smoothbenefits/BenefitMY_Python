from pdf_tk_engine import get_template


class PDFFormFillService(object):

    def fill_form(self, template_name, field_map):
        template = get_template(template_name)
        return template.render(field_map)
