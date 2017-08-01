import json
import responses
import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from app.views.reports.tests.test_mock_time_punch_card_app_base import TestMockTimePunchCardAppBase


class ConnectPayrollPeriodExportCsvTestCase(TestMockTimePunchCardAppBase):
    # your fixture files here
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user', '13_benefit_type',
                '17_supplemental_life_insurance_condition', '15_benefit_policy_key',
                '16_benefit_policy_type', 'sys_application_feature',
                '21_benefit_plan', '22_benefit_details', '26_supplemental_life_insurance',
                '31_company_benefit_plan_option', '32_enrolled', '34_company_user',
                '37_fsa_plan', '38_supplemental_life_rate', '39_company_supplement_life_insurance',
                '41_user_company_benefit_plan_option', '42_company_fsa', '43_fsa',
                '44_person_company_suppl_life', '45_suppl_life_beneficiary', '46_hra_plan',
                '47_company_hra_plan', '48_person_company_hra_plan', 'company_features',
                'life_insurance', 'ltd_insurance', 'std_insurance', 'waived_benefit', 'direct_deposit',
                'user_bank_account','77_integration_provider', '78_company_integration_provider']

    @responses.activate
    def test_get_connect_payroll_period_export_csv_success(self):
        week_start_date = datetime.date(2017, 1, 1)
        week_end_date = datetime.date(2017, 1, 7)
        mock_url = self._setup_mock_url(week_start_date, week_end_date, 1)
        mock_json = self._setup_mock_return_json([week_start_date], 1, 3)
        self.setup_mock_get(
            path=mock_url,
            return_json = mock_json)

        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_connect_payroll_period_export_csv_api',
                                               kwargs={
                                                'company_id': self.normalize_key(1),
                                                'from_year': '2017',
                                                'from_month': '1',
                                                'from_day': '1',
                                                'to_year': '2017',
                                                'to_month': '1',
                                                'to_day': '7'}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'], 'text/csv')
        else:
            self.assertFalse("login failed!")
