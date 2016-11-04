import StringIO

from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

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

        # Write the PDF data to the stream
        pdf_stream = StringIO.StringIO()
        pdf_stream.write(filled_pdf_form_data) 

        pdf_modification_service = PdfModificationService()
        # pdf_modification_service.place_text(
        #     pdf_stream,
        #     3,
        #     'Alibaba AAAAAAAAAAAAAAAAAAAAAAAAA',
        #     1,
        #     2.5,
        #     response)

        # pdf_modification_service.place_image(
        #     pdf_stream,
        #     3,
        #     'app/templates/PDF/test.png',
        #     1,
        #     2.5,
        #     3,
        #     3,
        #     response
        # )

        # TODO:
        # Figure out how to 
        #   1. Convert our signature svg data to image data stream
        #   2. Make reportlab able to draw image from image data stream.
        pdf_modification_service.place_image(
            pdf_stream,
            7,
            'app/templates/PDF/test_sig.png',
            1.766666667,
            3.133333333,
            3.9,
            0.3,
            response
        )

        return response
