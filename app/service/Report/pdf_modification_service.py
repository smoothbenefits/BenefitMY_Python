from pyPdf import PdfFileWriter, PdfFileReader
from app.service.Report.pdf_compose_service import (
    PdfComposeService,
    PlacementBounds
)
import StringIO


class PdfModificationService(object):

    def place_image(
        self,
        original_pdf_stream,
        image_stream,
        image_placements,
        output_stream):
        image_placement_operation = PDFImagePlacementOperation(image_stream, image_placements)
        self.modify_pdf_document_with_operation(
            original_pdf_stream,
            image_placement_operation,
            output_stream)

    def append_to_pdf_document(self, original_pdf_stream, pdf_composer_callback, output_stream):
        self._internal_modify_pdf_document(
            original_pdf_stream,
            lambda pdf_composer: self._advance_pdf_composer_page_for_append(original_pdf_stream, pdf_composer),
            pdf_composer_callback,
            output_stream
        )

    def _advance_pdf_composer_page_for_append(self, original_pdf_stream, pdf_composer):
        original_pdf_stream.seek(0)
        original_pdf = PdfFileReader(original_pdf_stream)

        for page_index in range(0, original_pdf.numPages):
            pdf_composer.start_new_page()

    def modify_pdf_document(self, original_pdf_stream, pdf_composer_callback, output_stream):
        self._internal_modify_pdf_document(
            original_pdf_stream,
            lambda pdf_composer: None,
            pdf_composer_callback,
            output_stream
        )
        
    def modify_pdf_document_with_operation(self, original_pdf_stream, pdf_operation, output_stream):
        self.modify_pdf_document(
            original_pdf_stream,
            lambda pdf_composer: pdf_operation.write_to_pdf(pdf_composer),
            output_stream)

    def _internal_modify_pdf_document(self, original_pdf_stream, pdf_composer_preconfig, pdf_composer_callback, output_stream):
        # Create a PDF canvas to hold the target drawing to be merged
        # on to the original
        packet = StringIO.StringIO()

        # Manipulate the PDF composer to apply modifications
        packet.seek(0)
        pdf_composer = PdfComposeService()
        pdf_composer.init_canvas(packet)
        pdf_composer_preconfig(pdf_composer)
        pdf_composer_callback(pdf_composer)
        pdf_composer.save()

        # Move to the beginning of the StringIO buffer
        # And initialize a PDF file reader to read that in
        # as source asset PDF to be merged into the original 
        packet.seek(0)
        source_pdf = PdfFileReader(packet)

        # Now read in the destination/original PDF as the merge target
        original_pdf_stream.seek(0)
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

        # If the modification doc has more pages than the original
        # also just append them to the resultant document
        for page_index in range(0, source_pdf.numPages):
            if (page_index >= original_pdf.numPages):
                page = source_pdf.getPage(page_index)
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
        self.placement_bounds = PlacementBounds(
            left_in_inch,
            bottom_in_inch,
            width_in_inch,
            height_in_inch
        )


class PDFOperationBase(object):
    def __init__(self):
        pass

    def write_to_pdf(self, pdf_composer):
        raise NotImplementedError()


class PDFImagePlacementOperation(PDFOperationBase):
    def __init__(self, image_stream, placements):
        super(PDFImagePlacementOperation, self).__init__()
        self.image_stream = image_stream
        self.placements = placements

    def write_to_pdf(self, pdf_composer):
        # Sorts the placements by page number
        sorted_placements = sorted(self.placements, key=lambda placement: placement.page_number)

        # Now for each of the placement, place the image
        current_page = 1
        for image_placement in sorted_placements:

            # Adding page to canvas until got to the page to place the 
            # next placement
            while(current_page < image_placement.page_number):
                pdf_composer.start_new_page()
                current_page = current_page + 1

            pdf_composer.place_image(self.image_stream, image_placement.placement_bounds)
