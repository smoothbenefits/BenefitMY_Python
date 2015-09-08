from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory
from app.models.company_1095_c import Company1095C, PERIODS

User = get_user_model()


class Form1095CView(ReportExportViewBase):

    def get(self, request, pk, format=None):
        model_factory = ReportViewModelFactory()
        person_info = model_factory.get_employee_person_info(pk)
        company_info = model_factory.get_employee_company_info(pk)

        company_model = self._get_company_by_user(pk)

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
        }

        index = 0
        for perd in PERIODS:
            comp_1095_c_for_period = Company1095C.objects.filter(company=company_model.id, period=perd)
            if comp_1095_c_for_period:
                field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_0{1}[0]'.format(1, 11 + index)
                fields[str(field_key)] = comp_1095_c_for_period[0].offer_of_coverage
                field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_0{1}[0]'.format(2, 25 + index)
                if index + 1 == len(PERIODS):
                    # This is not something we can control. However, for this particular field, 
                    # it does not follow the sequential number pattern. The number here is "300"
                    # Hence the special case
                    field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_300[0]'.format(2) 
                fields[str(field_key)] = comp_1095_c_for_period[0].employee_share
                field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_0{1}[0]'.format(3, 50 + index)
                fields[str(field_key)] = comp_1095_c_for_period[0].safe_harbor
            index += 1



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
