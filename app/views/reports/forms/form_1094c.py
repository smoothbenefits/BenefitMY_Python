from django.http import HttpResponse
from django.db.models import Min
from django.contrib.auth import get_user_model

from app.models.aca.company_1094_c_member_info import ELIGIBILITY_CERTIFICATIONS
from app.models.aca.company_1094_c_monthly_member_info import PERIODS
from app.service.Report.pdf_form_fill_service import PDFFormFillService
from ..report_export_view_base import ReportExportViewBase
from app.factory.report_view_model_factory import ReportViewModelFactory

User = get_user_model()
FORM_YEAR = 2015


class Form1094CView(ReportExportViewBase):

    def get(self, request, pk, format=None):

        model_factory = ReportViewModelFactory()
        company_info = model_factory.get_company_info(pk)
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
        }

        self._write_field_for_company_member_info(fields, company_1094c)
        self._write_field_for_company_monthly_info(fields, company_1094c.monthly_info)

        file_name_prefix = ''
        company_name = company_info.company_name
        if (company_name is not None):
            file_name_prefix = company_name

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name_prefix  +'_1094-C.pdf"'
        formService = PDFFormFillService()
        formService.fill_form_to_stream('PDF/1094c.pdf', fields, response)

        return response

    def _write_field_for_company_member_info(self, fields, company_1094c):
        # Total number of 1095-C submitted
        fields['topmostSubform[0].Page1[0].f1_17[0]'] = company_1094c.number_of_1095c
        # Total number of 1095-C submitted for ALE member
        fields['topmostSubform[0].Page1[0].f1_18[0]'] = company_1094c.number_of_1095c

        # Is authoritative transmittal
        if (company_1094c.authoritative_transmittal):
            fields['topmostSubform[0].Page1[0].c1_03[0]'] = '1'

        if company_1094c.member_of_aggregated_group:
            fields['topmostSubform[0].Page1[0].c1_08[0]'] = 'Yes'
        else:
            fields['topmostSubform[0].Page1[0].c1_08[1]'] = 'No'

        self._write_field_for_eligibility_certification(fields, company_1094c)

    def _write_field_for_eligibility_certification(self, fields, company_1094c):
        for i in range(len(ELIGIBILITY_CERTIFICATIONS)):
            cert = ELIGIBILITY_CERTIFICATIONS[i]
            if company_1094c.certifications_of_eligibility == cert:
                key = 'topmostSubform[0].Page1[0].c1_0{0}[0]'.format(i + 4)
                fields[str(key)] = 'Yes'

    def _write_field_for_company_monthly_info(self, fields, monthly_info):
        # All 12 month case
        all_year_period = PERIODS[0]
        all_year_data = next((month for month in monthly_info if month.period == all_year_period), None)
        if (all_year_data and not all_year_data.is_empty):
            self._write_field_for_all_year_info(fields, all_year_data)

        for i in range(1, 13):
            period = PERIODS[i]
            period_data = next((month for month in monthly_info if month.period == period), None)
            if not period_data.is_empty:
                self._write_field_for_monthly_data(i, fields, period_data)

    def _write_field_for_all_year_info(self, fields, all_year_data):

        # minimum essential coverage
        if all_year_data.minimum_essential_coverage:
            fields['topmostSubform[0].Page2[0].Table1[0].Row1[0].p2-cb1[0]'] = 'Yes'
        else:
            fields['topmostSubform[0].Page2[0].Table1[0].Row1[0].p2-cb1[1]'] = 'No'

        # full time employee count
        fields['topmostSubform[0].Page2[0].Table1[0].Row1[0].f2_300[0]'] = all_year_data.fulltime_employee_count

        # total employee count
        fields['topmostSubform[0].Page2[0].Table1[0].Row1[0].f2_01[0]'] = all_year_data.total_employee_count

        # a member of aggregated group
        if all_year_data.aggregated_group:
            fields['topmostSubform[0].Page2[0].Table1[0].Row1[0].c2_01[0]'] = '1'

        # section 4890H section indicator
        fields['topmostSubform[0].Page2[0].Table1[0].Row1[0].f2_02[0]'] = all_year_data.section_4980h_transition_relief

    def _write_field_for_monthly_data(self, index, fields, period_info):
        row_num = index + 1
        # for some reason, number on the fifth row jump a number
        padding = 1 if row_num  > 4 else 0
        # minimum essential coverage
        if period_info.minimum_essential_coverage:
            key = 'topmostSubform[0].Page2[0].Table1[0].Row{0}[0].p2-cb{0}[0]'.format(row_num)
            fields[str(key)] = 'Yes'
        else:
            key = 'topmostSubform[0].Page2[0].Table1[0].Row{0}[0].p2-cb{0}[1]'.format(row_num)
            fields[str(key)] = 'No'

        # full time employee count
        number = '{0:02d}'.format(3 * (row_num - 1) + padding)
        key = 'topmostSubform[0].Page2[0].Table1[0].Row{0}[0].f2_{1}[0]'.format(row_num, number)
        fields[str(key)] = period_info.fulltime_employee_count
        print 'FILLED ' + key + ' with ' + str(period_info.fulltime_employee_count)

        # total employee count
        number = '{0:02d}'.format(3 * (row_num - 1) + 1 + padding)
        key = 'topmostSubform[0].Page2[0].Table1[0].Row{0}[0].f2_{1}[0]'.format(row_num, number)
        fields[str(key)] = period_info.total_employee_count
        print 'FILLED ' + key + ' with ' + str(period_info.total_employee_count)

        # a member of aggregated group
        if period_info.aggregated_group:
            number = '{0:02d}'.format(row_num)
            key = 'topmostSubform[0].Page2[0].Table1[0].Row{0}[0].c2_{1}[0]'.format(row_num, number)
            fields[str(key)] = '1'

        # section 4890H section indicator
        number = '{0:02d}'.format(3 * (row_num - 1) + 2 + padding)
        key = 'topmostSubform[0].Page2[0].Table1[0].Row{0}[0].f2_{1}[0]'.format(row_num, number)
        fields[str(key)] = period_info.section_4980h_transition_relief
        print 'FILLED ' + key + ' with ' + str(period_info.section_4980h_transition_relief)
