import StringIO
import cairosvg

from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.models.w4 import (
    W4_MARRIAGE_STATUS_SINGLE,
    W4_MARRIAGE_STATUS_MARRIED,
    W4_MARRIAGE_STATUS_MARRIED_HIGH_SINGLE
)
from app.models.signature import Signature
from app.service.pdf_processing.pdf_form_fill_service import PDFFormFillService
from app.service.signature_service import (
    SignatureService,
    PdfFormSignaturePlacements
)
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory
from datetime import date, timedelta
from django.http import Http404

User = get_user_model()


class FormW4View(ReportExportViewBase):

    def get(self, request, pk, format=None):

        employee_user_id = pk
        model_factory = ReportViewModelFactory()
        person_info = model_factory.get_employee_person_info(employee_user_id)
        company_info = model_factory.get_employee_company_info(employee_user_id)
        w4_info = model_factory.get_employee_w4_data(employee_user_id)

        # Build employer info line
        employer_line = (company_info.company_name 
            + ', ' + company_info.get_full_street_address()
            + ', ' + company_info.city
            + ', ' + company_info.state + ' ' + company_info.zipcode)
 
        # Populate the form fields
        fields = {
            'topmostSubform[0].Page1[0].Line1[0].f1_10_0_[0]': person_info.last_name,
            'topmostSubform[0].Page1[0].Line1[0].f1_09_0_[0]': person_info.first_name,
            'topmostSubform[0].Page1[0].Line1[0].f1_11_0_[0]': person_info.get_full_street_address(),
            'topmostSubform[0].Page1[0].Line1[0].f1_12_0_[0]': person_info.get_city_state_zipcode(),
            'topmostSubform[0].Page1[0].f1_13_0_[0]': person_info.ssn,
            'topmostSubform[0].Page1[0].f1_17_0_[0]': employer_line,
            'topmostSubform[0].Page1[0].f1_19_0_[0]': company_info.ein
        }

        if (w4_info):
            fields['topmostSubform[0].Page1[0].f1_14_0_[0]'] = w4_info.total_points
            fields['topmostSubform[0].Page1[0].f1_15_0_[0]'] = w4_info.extra_amount

            if (w4_info.marriage_status == W4_MARRIAGE_STATUS_SINGLE):
                fields['topmostSubform[0].Page1[0].c1_01[0]'] = '1'
            elif(w4_info.marriage_status == W4_MARRIAGE_STATUS_MARRIED):
                fields['topmostSubform[0].Page1[0].c1_01[1]'] = '2'
            elif(w4_info.marriage_status == W4_MARRIAGE_STATUS_MARRIED_HIGH_SINGLE):
                fields['topmostSubform[0].Page1[0].c1_01[2]'] = '3'

        file_name_prefix = ''
        full_name = person_info.get_full_name()
        if (full_name is not None):
            file_name_prefix = full_name

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name_prefix  +'_w4.pdf"'
        
        # Now produce the PDF with information filled
        formService = PDFFormFillService()
        pdf_stream = formService.get_filled_form_stream('PDF/tax/w4.pdf', fields)

        # Now utilize the signature service to apply the user's signature
        # if applicable
        signature_service = SignatureService()
        sign_success = signature_service.sign_pdf_stream(
            pk,
            pdf_stream,
            PdfFormSignaturePlacements.Form_W4,
            response
        )

        if (not sign_success):
            response.write(pdf_stream.read())

        return response
