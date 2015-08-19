from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
from django.db.models import Count, Min
from django.contrib.auth import get_user_model

from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ..report_export_view_base import ReportExportViewBase

User = get_user_model()


class Form1095CView(ReportExportViewBase):

    def get(self, request, pk, format=None):
        person_info = self._get_person_basic_info_by_user(pk)
        company_model = self._get_company_by_user(pk)
        company_info = self._get_company_basic_info(company_model)

        # Populate the form fields
        fields = {
            # Name Employee
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_002[0]': person_info.get_full_name(),
            # SSN
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_003[0]': person_info.ssn,
            # Street Address
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_004[0]': person_info.get_full_street_address(),
            # City
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_005[0]': person_info.city,
            # State
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_006[0]': person_info.state,
            # Country and Zip or Foreign Postcode
            'topmostSubform[0].Page1[0].EmployeeName[0].f1_007[0]': person_info.get_country_and_zipcode(),

            # Name Employer
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_008[0]': company_info.company_name,
            # EIN
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_009[0]': company_info.ein,
            # Street Address
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_010[0]': company_info.get_full_street_address(),
            # Contact Phone Number
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_011[0]': company_info.contact_phone,
            # City
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_012[0]': company_info.city,
            # State
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_013[0]': company_info.state,
            # Country and Zip or Foreign Postcode
            'topmostSubform[0].Page1[0].EmployerIssuer[0].f1_014[0]': company_info.get_country_and_zipcode(),

            # Code Row
            'topmostSubform[0].Page1[0].Part2Table[0].BodyRow1[0].f1_011[0]': company_info.offer_of_coverage_code,

            # Premium Row
            'topmostSubform[0].Page1[0].Part2Table[0].BodyRow2[0].f1_025[0]': self._get_minimum_monthly_employee_cost_medical(company_model),
        }

        file_name_prefix = ''
        full_name = person_info.get_full_name()
        if (full_name is not None):
            file_name_prefix = full_name

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name_prefix  +'_1095-C.pdf"'
        formService = PDFFormFillService()
        formService.fill_form('PDF/1095c.pdf', fields, response)

        return response

    def _get_minimum_monthly_employee_cost_medical(self, company_model):
        result = ''

        if (company_model):
            benefit_options = company_model.company_benefit.filter(benefit_plan__benefit_type__name = 'Medical', benefit_option_type='individual')
            if (len(benefit_options) > 0):
                min_cost = benefit_options.aggregate(Min('employee_cost_per_period'))['employee_cost_per_period__min']
                result = "{:.2f}".format(float(min_cost))

        return result
