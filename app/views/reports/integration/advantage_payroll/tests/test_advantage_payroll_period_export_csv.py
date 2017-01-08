import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class AdvantagePayrollPeriodExportCsvTestCase(TestCase, ViewTestBase):
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
                'user_bank_account']

    def test_get_advantage_payroll_period_export_csv_success(self):
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_advantage_payroll_period_export_csv_api',
                                               kwargs={'company_id': self.normalize_key(1)}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'], 'text/csv')
        else:
            self.assertFalse("login failed!")
