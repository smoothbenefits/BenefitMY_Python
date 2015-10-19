from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory

User = get_user_model()
FORM_YEAR = 2015


class Form1094CView(ReportExportViewBase):

    def get(self, request, pk, format=None):

        model_factory = ReportViewModelFactory()
        company_info = model_factory.get_employee_company_info(pk)
        company_1094c = model_factory.get_company_1094_c_data(pk)

        # Populate the form fields
        fields = {
            # Name Employer
            'topmostSubform[0].Page1[0].Name[0].f1_01[0]': company_info.company_name,
            # EIN
            'topmostSubform[0].Page1[0].Name[0].f1_02[0]': company_info.ein,
            # Street Address
            'topmostSubform[0].Page1[0].Name[0].f1_03[0]': company_info.get_full_street_address(),
            # City
            'topmostSubform[0].Page1[0].Name[0].f1_04[0]': company_info.city,
            # State
            'topmostSubform[0].Page1[0].Name[0].f1_05[0]': company_info.state,
            # Country and Zip or Foreign Postcode
            'topmostSubform[0].Page1[0].Name[0].f1_06[0]': company_info.get_country_and_zipcode(),
            # Contact Phone Number
            'topmostSubform[0].Page1[0].Name[0].f1_07[0]': company_info.get_contact_full_name(),
            # Contact Phone Number
            'topmostSubform[0].Page1[0].Name[0].f1_08[0]': company_info.contact_phone,

            ##############################
            ## TODO:
            ##     Dummy data starts here
            ##############################

            # Total number of 1095-C submitted
            'topmostSubform[0].Page1[0].f1_17[0]': company_1094c.number_of_1095c,
            # Is authoritative transmittal
            'topmostSubform[0].Page1[0].c1_03[0]': '1',
            # Total number of 1095-C submitted for ALE member
            'topmostSubform[0].Page1[0].f1_18[0]': company_1094c.number_of_1095c,
            # Is ALE Member a member of an Aggregated ALE Group
            'topmostSubform[0].Page1[0].c1_08[1]': 'No',
            # Certifications of Eligibility
            'topmostSubform[0].Page1[0].c1_06[0]': 'Yes',

            # ALE member info
            ## All 12 Months
            'topmostSubform[0].Page2[0].Table1[0].Row1[0].p2-cb1[0]': 'Yes',
            'topmostSubform[0].Page2[0].Table1[0].Row1[0].f2_01[0]': '1000',
            'topmostSubform[0].Page2[0].Table1[0].Row1[0].c2_01[0]': '1',
            'topmostSubform[0].Page2[0].Table1[0].Row1[0].f2_02[0]': 'BBBBB',
        }

        file_name_prefix = ''
        company_name = company_info.company_name
        if (company_name is not None):
            file_name_prefix = company_name

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name_prefix  +'_1094-C.pdf"'
        formService = PDFFormFillService()
        formService.fill_form('PDF/1094c.pdf', fields, response)

        return response
