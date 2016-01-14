from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory
from app.models.aca.company_1095_c import PERIODS
from app.models.employee_profile import EmployeeProfile
from datetime import date, timedelta
from copy import deepcopy
from django.http import Http404


User = get_user_model()
FORM_YEAR = 2015


class Form1095CView(ReportExportViewBase):

    def get(self, request, pk, format=None):
        employee_user_id = pk
        model_factory = ReportViewModelFactory()
        person_info = model_factory.get_employee_person_info(employee_user_id)
        company_info = model_factory.get_employee_company_info(employee_user_id)

        company_model = self._get_company_by_user(employee_user_id)
        if not company_model:
            raise Http404

        employee_profile = self._get_employee_profile_by_user_id(employee_user_id, company_model.id)

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
        if employee_profile:
            # use employee user id and company id to retrieve employee's information for form 1095C
            period_map = self._get_1095C_benefits_data(employee_user_id,
                                                       company_model.id,
                                                       employee_profile.start_date,
                                                       employee_profile.end_date)
            map_size = len(period_map)
            for period in period_map:
                index = self._write_field_for_benefit_data(fields, period['benefit_data'], index, map_size)
        else:
            company_1095c_collection = model_factory.get_employee_1095_c_data(employee_user_id, company_model.id)
            for perd in PERIODS:
                comp_1095_c_for_period = next(datum for datum in company_1095c_collection if datum.period == perd)
                if comp_1095_c_for_period:
                    index = self._write_field_for_benefit_data(fields, comp_1095_c_for_period, index, len(PERIODS))


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

    def _get_employee_profile_by_person_company(person_id, company_id):
        profile = EmployeeProfile.objects.filter(person=person_id, company=company_id)
        if profile:
            return profile[0]

    def _write_field_for_benefit_data(self, fields, benefit_data, index, size):
        if benefit_data:
            field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_0{1}[0]'.format(1, 11 + index)
            fields[str(field_key)] = benefit_data.offer_of_coverage
            field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_0{1}[0]'.format(2, 25 + index)
            if index + 1 == size:
                # This is not something we can control. However, for this particular field,
                # it does not follow the sequential number pattern. The number here is "300"
                # Hence the special case
                field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_300[0]'.format(2)
            fields[str(field_key)] = benefit_data.employee_share
            field_key = 'topmostSubform[0].Page1[0].Part2Table[0].BodyRow{0}[0].f1_0{1}[0]'.format(3, 50 + index)
            fields[str(field_key)] = benefit_data.safe_harbor
        index += 1
        return index

    def _get_1095C_benefits_data(self, user_id, comp_id, emp_start_date, emp_end_date):
        # If the dates are not specified, we use really wide range defaults
        if not emp_start_date:
            emp_start_date = date(1900, 1, 1)
        if not emp_end_date:
            emp_end_date = date(2500, 12, 31)
        if emp_start_date > emp_end_date:
            raise ValueError('The employee start_date is later than employee end_date!')

        period_date_map = []
        period_date_map.append({'period':PERIODS[0], 'date':None})
        for x in range(1, 13):
            period_date_map.append({'period':PERIODS[x], 'date': date(FORM_YEAR, x, 1)})

        model_factory = ReportViewModelFactory()
        employee_1095c_data = model_factory.get_employee_1095_c_data(user_id, comp_id)

        # Start the whole year case
        whole_year_period_date = period_date_map[0]
        # This record down the "all 12 month" data
        whole_year_benefit_data = next((datum for datum in employee_1095c_data if datum.period == whole_year_period_date['period']), None)
        # Check to see if the employee is active for the whole year
        whole_year = emp_start_date <= date(FORM_YEAR, 1, 31) and emp_end_date >= date(FORM_YEAR, 12, 1)
        if whole_year_benefit_data and whole_year:
            # We only fill out the "All 12 month" if employee is active for the whole year and
            # the company filled data has the "All 12 month" column specified
            whole_year_period_date['benefit_data'] = whole_year_benefit_data
        else:
            whole_year_period_date['benefit_data'] = None
        # End of whole year case
        for i in range(1, 13):
            period_date = period_date_map[i]
            benefit_data = None
            cur_period_data = None
            if employee_1095c_data:
                cur_period_data = next((datum for datum in employee_1095c_data if datum.period == period_date['period']), None)
            if not (whole_year and whole_year_benefit_data) and \
                emp_end_date >= period_date['date'] and emp_start_date < self._get_next_month_start(period_date['date']):
                # We should not record any data, unless within this period the employee is active
                # Note if employee is active starting the end of the month, the employee is active in that month
                # if the employee is terminated at the beginning of the month, the employee is active in that month
                if whole_year_benefit_data:
                    # we choose to record the "All 12 month" column data
                    benefit_data = whole_year_benefit_data
                elif cur_period_data:
                    # We record whatever the company specified
                    benefit_data = cur_period_data

            period_date['benefit_data'] = benefit_data

        return period_date_map

    def _get_next_month_start(self, start_date):
        # Gets the first day of the next month from input date
        next_month_date = start_date + timedelta(days=32)
        next_month_first = next_month_date.replace(day=1)
        return next_month_first
