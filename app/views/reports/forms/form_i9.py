import StringIO
import cairosvg

from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.models.signature import Signature
from app.service.Report.pdf_form_fill_service import PDFFormFillService
from app.service.Report.pdf_modification_service import PdfModificationService
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory
from datetime import date, timedelta
from django.http import Http404

User = get_user_model()


class FormI9View(ReportExportViewBase):

    def get(self, request, pk, format=None):

        # Populate the form fields
        fields = {
            'form1[0].#subform[6].FamilyName[0]': 'Alibaba'
        }

        output_file_name_prefix = 'test'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + output_file_name_prefix  +'_I9.pdf"'
        formService = PDFFormFillService()
        filled_pdf_form_data = formService.fill_form('PDF/i-9.pdf', fields)

        # Now attempt at electronic sign the form if there is signature
        # for the user on file, else just provide the unsigned form
        user_signature_list = Signature.objects.filter(user=pk)
        if len(user_signature_list) > 0: 
            signature = user_signature_list[0].signature
            # TODO!!!
            # Write service to parse the svg out of the signature data
            signature_svg = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="214" height="62"><path fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 82 61 c -0.23 0 -8.84 0.68 -13 0 c -9.87 -1.61 -19.9 -5.08 -30 -7 c -3.95 -0.75 -8.03 -0.36 -12 -1 c -4.4 -0.7 -8.62 -1.85 -13 -3 c -2.08 -0.55 -4.35 -0.98 -6 -2 c -2.41 -1.48 -6.08 -4.01 -7 -6 c -0.71 -1.53 -0.4 -6.18 1 -7 c 5.87 -3.44 18.54 -7.27 28 -10 c 5.49 -1.59 11.28 -2.78 17 -3 c 28.52 -1.11 62.18 -1.53 86 -1 c 1.38 0.03 4.37 2.36 4 3 c -1.06 1.82 -7.07 6.56 -11 9 c -5.56 3.45 -11.84 6.95 -18 9 c -8.47 2.82 -24.76 6.45 -27 6 c -0.99 -0.2 4.31 -7.31 7 -10 c 2.69 -2.69 9.6 -5.68 10 -7 c 0.25 -0.83 -5.37 -1.73 -7 -3 c -0.96 -0.75 -2.11 -2.9 -2 -4 c 0.16 -1.65 1.54 -5.4 3 -6 c 3.04 -1.25 10.44 -2.31 14 -1 c 5.08 1.86 10.87 7.72 16 12 c 2.9 2.42 5.09 5.82 8 8 c 3.57 2.68 12.17 7.17 12 7 c -0.21 -0.21 -9.76 -5.5 -14 -9 c -9.02 -7.44 -18.75 -16.02 -26 -24 c -2.02 -2.22 -4.41 -7.64 -4 -9 c 0.29 -0.98 4.72 -1 7 -1 c 3.25 0 7.15 -0.1 10 1 c 5.21 2 10.79 5.61 16 9 c 9.37 6.1 18.32 12.37 27 19 c 2.6 1.99 4.48 5.27 7 7 c 2.51 1.72 7.09 2.47 9 4 c 0.8 0.64 0.49 4.07 1 4 c 0.97 -0.14 3.83 -3.53 6 -5 c 8.26 -5.59 25.77 -15.96 25 -16 c -1.18 -0.07 -43.69 14.02 -43 15 c 0.76 1.08 42.87 -5 50 -5 l -1 5"/></svg> '

            # Write the svg to an image stream
            signature_image_stream = StringIO.StringIO()
            cairosvg.svg2png(bytestring=signature_svg.encode('UTF-8'), write_to=signature_image_stream)
            signature_image_stream.seek(0)

            # Write the PDF data to the stream
            pdf_stream = StringIO.StringIO()
            pdf_stream.write(filled_pdf_form_data) 
            pdf_stream.seek(0)

            # Utilize the PDF modification service to place the signature 
            # onto the form
            pdf_modification_service = PdfModificationService()

            # Place the signature image onto the PDF form
            pdf_modification_service.place_image(
                pdf_stream,
                7,
                signature_image_stream,
                1.766666667,
                3.133333333,
                3.9,
                0.3,
                response
            )
        else :
            response.write(filled_pdf_form_data)

        return response
