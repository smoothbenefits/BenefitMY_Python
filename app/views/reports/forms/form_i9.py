import StringIO
import cairosvg

from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.models.signature import Signature
from app.service.Report.pdf_form_fill_service import PDFFormFillService
from app.service.signature_service import (
    SignatureService,
    PdfFormSignaturePlacements
)
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory
from datetime import date, timedelta
from django.http import Http404

User = get_user_model()


class FormI9View(ReportExportViewBase):

    def get(self, request, pk, format=None):

        # Populate the form fields
        fields = {
            'form1[0].#subform[6].FamilyName[0]': 'Zhang',
            'form1[0].#subform[6].GivenName[0]': 'Alibaba'
        }

        output_file_name_prefix = 'test'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + output_file_name_prefix  +'_I9.pdf"'
        
        # Now produce the PDF with information filled
        formService = PDFFormFillService()
        pdf_stream = formService.get_filled_form_stream('PDF/i-9.pdf', fields)

        # Now utilize the signature service to apply the user's signature
        # if applicable
        signature_service = SignatureService()
        sign_success = signature_service.sign_pdf_stream(
            pk,
            pdf_stream,
            PdfFormSignaturePlacements.Form_I9,
            response
        )

        if (not sign_success):
            response.write(pdf_stream.read())

        return response
