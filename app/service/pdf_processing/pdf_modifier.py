from pyPdf import PdfFileWriter, PdfFileReader
from app.service.pdf_processing.pdf_composer import (
    PdfComposer,
    PlacementBounds
)
import StringIO

''' A utility class to apply modifications to an existing 
    PDF file (stream), with a builder pattern
'''
class PdfModifier(object):
    def __init__(self, original_pdf_stream):
        self._original_pdf_stream = original_pdf_stream
        self._original_pdf_stream.seek(0)

        # initialize a buffer stream to compose the modification
        # that to be merged later
        self._modification_stream = StringIO.StringIO()

    ''' Apply specified list of operations to the PDF
        @param modification_operations list of predefined PDF operations
               (concrete implementations of 'PDFOperationBase')
    '''
    def with_modification_operations(self, modification_operations):
        for modification_operation in modification_operations:
            # start a new composer and apply the operation logic
            # polymophically 
            pdf_composer = self._init_pdf_composer()
            modification_operation.write_to_pdf(pdf_composer)
            pdf_composer.save()

        return self

    def with_modifications(self, pdf_composer_callback):
        pdf_composer = self._init_pdf_composer()
        pdf_composer_callback(pdf_composer)
        pdf_composer.save()

        return self

    ''' The output method of the builder, to actually  
    '''
    def build_output_pdf(self, output_stream):

        # Move to the beginning of the StringIO buffer
        # And initialize a PDF file reader to read that in
        # as source asset PDF to be merged into the original 
        self._modification_stream.seek(0)
        source_pdf = PdfFileReader(self._modification_stream)

        # Now read in the destination/original PDF as the merge target
        self._original_pdf_stream.seek(0)
        original_pdf = self._get_pdf_reader(self._original_pdf_stream)

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

    def get_num_pages_in_original(self):
        self._original_pdf_stream.seek(0)
        original_pdf = self._get_pdf_reader(self._original_pdf_stream)
        return original_pdf.numPages

    def _get_pdf_reader(self, pdf_stream):
        pdf = PdfFileReader(pdf_stream)
        if pdf.isEncrypted:
            pdf.decrypt("")
        return pdf

    def _init_pdf_composer(self):
        self._modification_stream.seek(0)
        return PdfComposer(self._modification_stream)


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
