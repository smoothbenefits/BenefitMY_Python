import StringIO
import cairosvg

from django.conf import settings
from django.contrib.auth import get_user_model

from app.models.signature import Signature
from app.service.Report.pdf_modification_service import PdfModificationService

User = get_user_model()


class SignatureService(object):

    ''' Get an image stream (in StringIO) contains the users' signature
        if exists and can be successfully read into an image. Or returns None.
    ''' 
    def get_user_signature_image_stream(self, user_id):
        try :
            user_signature_list = Signature.objects.filter(user=user_id)
            if len(user_signature_list) > 0: 
                signature = user_signature_list[0].signature

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

            return None
        except:
            return None

    ''' Sign the PDF represented with the given PDF stream (a file object or a
        StringIO) with the signature with the given user_id if found.
        Return True if signature was applied successfully, False otherwise.

        Note: Per PDF convention, the x and y identifies the *bottom left* corner
              of the signature area.
    '''
    def sign_pdf_stream(
        self,
        user_id,
        pdf_stream,
        page_num,
        left_in_inch,
        bottom_in_inch,
        width_in_inch,
        height_in_inch,
        output_stream):
        signature_image_stream = self.get_user_signature_image_stream(user_id)
        if (signature_image_stream):
            # Utilize the PDF modification service to place the signature 
            # onto the form
            pdf_modification_service = PdfModificationService()

            # Place the signature image onto the PDF form
            pdf_modification_service.place_image(
                pdf_stream,
                page_num,
                signature_image_stream,
                left_in_inch,
                bottom_in_inch,
                width_in_inch,
                height_in_inch,
                output_stream)

            return True

        return False
