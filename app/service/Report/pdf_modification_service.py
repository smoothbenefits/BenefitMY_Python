from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


class PdfModificationService(object):
    
    def place_image_fake(self, pdf_file_path, image_file_path, output_stream):
        a = Image.open(image_file_path)  
        a.drawHeight = 0.3*inch
        a.drawWidth = 2*inch
        c = canvas.Canvas(output_stream, pagesize=letter)
        c.save()
        return None

    def place_image(
        self,
        original_pdf_stream,
        target_page_number,
        image_file_path,
        x_in_inch,
        y_in_inch,
        width_in_inch,
        height_in_inch,
        output_stream):
        self._merge_canvas_to_pdf(
            original_pdf_stream,
            (lambda canvas: self._draw_image_on_canvas(
                canvas,
                image_file_path,
                x_in_inch,
                y_in_inch,
                width_in_inch,
                height_in_inch
            )),
            target_page_number,
            output_stream)

    def _draw_image_on_canvas(
        self,
        canvas,
        image_file_path,
        x_in_inch,
        y_in_inch,
        width_in_inch,
        height_in_inch):
        image = ImageReader(open(image_file_path, 'rb'))
        canvas.drawImage(
            image,
            x_in_inch * inch,
            y_in_inch * inch,
            width_in_inch * inch,
            height_in_inch * inch,
            preserveAspectRatio=True,
            mask='auto')

    def place_text(
        self,
        original_pdf_stream,
        target_page_number,
        text,
        x_in_inch,
        y_in_inch,
        output_stream):
        self._merge_canvas_to_pdf(
            original_pdf_stream,
            (lambda canvas: canvas.drawString(x_in_inch*inch, y_in_inch*inch, text)),
            target_page_number,
            output_stream)
        
    def _merge_canvas_to_pdf(self, original_pdf_stream, canvas_operation, target_page_number, output_stream):
        
        # Create a PDF canvas to hold the target drawing to be merged
        # on to the original
        packet = StringIO.StringIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Invoke delegation logic to operate on the canvas
        # E.g. Draw an image at the desired place on the page
        canvas_operation(can)
        can.save()

        # Move to the beginning of the StringIO buffer
        # And initialize a PDF file reader to read that in
        # as source asset PDF to be merged into the original 
        packet.seek(0)
        source_pdf = PdfFileReader(packet)

        # Now read in the destination/original PDF as the merge target
        original_pdf = PdfFileReader(original_pdf_stream)

        # Now create the output PDF as the merge result holder
        output_pdf = PdfFileWriter()

        # Enumerate through the list of pages from the original PDF
        #  * Merge the specified page, and
        #  * For other pages, simply add them as is to the new PDF
        for page_index in range(0, original_pdf.numPages):    
            page = original_pdf.getPage(page_index)
            if (page_index == target_page_number - 1):
                page.mergePage(source_pdf.getPage(0))
            output_pdf.addPage(page)

        # Finally, write the result PDF to the given output stream
        output_pdf.write(output_stream)
