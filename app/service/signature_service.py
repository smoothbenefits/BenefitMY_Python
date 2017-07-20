import StringIO
import cairosvg

from django.conf import settings
from django.contrib.auth import get_user_model

from app.models.signature import Signature
from app.service.Report.pdf_modification_service import (
    PdfModificationService,
    ImagePlacement,
    PDFImagePlacementOperation
)
from app.factory.report_view_model_factory import ReportViewModelFactory

User = get_user_model()


# Define 

class SignatureService(object):

    ''' Get an image stream (in StringIO) contains the users' signature
        if exists and can be successfully read into an image. Or returns None.
    ''' 
    def get_user_signature_image_stream(self, user_id):
        try :
            user_signature_list = Signature.objects.filter(user=user_id)
            if len(user_signature_list) > 0: 
                signature_model = user_signature_list[0]

                return self.get_user_signature_image_stream_from_signature_model(signature_model)

            return None
        except:
            return None

    ''' Get an image stream (in StringIO) contains the users' signature
        from a signature model
    ''' 
    def get_user_signature_image_stream_from_signature_model(self, signature_model):
        try :
            signature = signature_model.signature

            # Now substring on our stored signature data to locate only
            # the svg data
            svg_start_index = signature.find('<svg')
            if (svg_start_index < 0):
                return None

            signature_svg = signature[svg_start_index:]

            # Write the svg to an image stream
            signature_image_stream = StringIO.StringIO()
            cairosvg.svg2png(bytestring=signature_svg.encode('UTF-8'), write_to=signature_image_stream)
            signature_image_stream.seek(0)

            return signature_image_stream
        except:
            return None

    ''' Sign the PDF represented with the given PDF stream (a file object or a
        StringIO) with the signature with the given user_id if found.
        Return True if signature was applied successfully, False otherwise.

        The signature would be placed for all specified placements in the list
        passed in.
    '''
    def sign_pdf_stream(
        self,
        user_id,
        pdf_stream,
        signature_placements,
        output_stream):
        signature_image_stream = self.get_user_signature_image_stream(user_id)
        if (signature_image_stream):
            # Utilize the PDF modification service to place the signature 
            # onto the form
            pdf_modification_service = PdfModificationService()

            # Place the signature image onto the PDF form
            pdf_modification_service.place_image(
                pdf_stream,
                signature_image_stream,
                signature_placements,
                output_stream)

            return True

        return False

    def append_signature_page(
        self,
        pdf_stream,
        user_id,
        signature_date,
        output_stream):
        # get signature image
        signature_image_stream = self.get_user_signature_image_stream(user_id)
        if (not signature_image_stream):
            return

        # get signature owner's full name
        view_model_factory = ReportViewModelFactory()
        person_info = view_model_factory.get_employee_person_info(user_id)
        full_name = person_info.get_full_name()

        # get date display text
        date_text = signature_date.strftime("%m/%d/%Y")

        # Modify the PDF
        pdf_modification_service = PdfModificationService()
        pdf_modification_service.append_to_pdf_document(
            pdf_stream,
            lambda pdf_composer: self._write_signature_page(pdf_composer, signature_image_stream, full_name, date_text),
            output_stream
        )

        return

    def _write_signature_page(self, pdf_composer, signature_image_stream, full_name, date_text):
        pdf_composer.set_font(22)
        pdf_composer.write_line(['Signature Page'])
        pdf_composer.draw_line()
        pdf_composer.start_new_line()

        pdf_composer.set_font(14)
        pdf_composer.write_line(['Full Name:   ', full_name])
        pdf_composer.start_new_line()
        pdf_composer.write_line(['Signature: '])
        pdf_composer.draw_image(signature_image_stream, 3.0, 1.5)
        pdf_composer.start_new_line()
        pdf_composer.write_line(['Date:   ', date_text])

''' A class to hold constants representing the pre-identified list
    of placements for signature onto various of PDF forms
'''
class PdfFormSignaturePlacements(object):

    Form_W4 = [
        ImagePlacement(1, 2.7, 0.85, 3.36666667, 0.35)
    ]
