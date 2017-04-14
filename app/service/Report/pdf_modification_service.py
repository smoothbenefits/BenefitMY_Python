from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


class PdfModificationService(object):

    def place_image(
        self,
        original_pdf_stream,
        image_stream,
        image_placements,
        output_stream):
        self._merge_canvas_to_pdf(
            original_pdf_stream,
            (lambda canvas: self._draw_image_on_canvas(
                canvas,
                image_stream,
                image_placements
            )),
            output_stream)

    def _draw_image_on_canvas(
        self,
        canvas,
        image_stream,
        image_placements):

        # Read in the image to place
        image = ImageReader(image_stream)

        # Sorts the placements by page number
        sorted_placements = sorted(image_placements, key=lambda placement: placement.page_number)

        # Now for each of the placement, place the image
        current_page = 1
        for image_placement in sorted_placements:

            # Adding page to canvas until got to the page to place the 
            # next placement
            while(current_page < image_placement.page_number):
                canvas.showPage()
                current_page = current_page + 1

            canvas.drawImage(
                image,
                image_placement.left_in_inch * inch,
                image_placement.bottom_in_inch * inch,
                image_placement.width_in_inch * inch,
                image_placement.height_in_inch * inch,
                preserveAspectRatio=True,
                mask='auto')
        
    def _merge_canvas_to_pdf(self, original_pdf_stream, canvas_operation, output_stream):
        
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
            if (page_index < source_pdf.numPages):
                page.mergePage(source_pdf.getPage(page_index))
            output_pdf.addPage(page)

        # Finally, write the result PDF to the given output stream
        output_pdf.write(output_stream)


''' A class representing an image placement(bounds) on PDF

    Note: Per PDF convention, the x and y identifies the *bottom left* corner
              of the signature area.
''' 
class ImagePlacement(object):
    def __init__(self, page_number, left_in_inch, bottom_in_inch, width_in_inch, height_in_inch):
        self.page_number = page_number
        self.left_in_inch = left_in_inch
        self.bottom_in_inch = bottom_in_inch
        self.width_in_inch = width_in_inch
        self.height_in_inch = height_in_inch
