import StringIO

from pdf_tk_engine import get_template


class PDFFormFillService(object):

    def get_filled_form_stream(self, template_name, field_map):
        pdf_stream = StringIO.StringIO()
        self.fill_form_to_stream(template_name, field_map, pdf_stream) 
        pdf_stream.seek(0)

        return pdf_stream

    def fill_form_to_stream(self, template_name, field_map, output_stream):
        template = get_template(template_name)
        output_stream.write(template.render(field_map))
