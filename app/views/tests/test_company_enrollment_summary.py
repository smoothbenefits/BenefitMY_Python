import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class CompanyEnrollmentSummaryTestCase(TestCase, ViewTestBase):
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
                'life_insurance', 'ltd_insurance', 'std_insurance', 'waived_benefit']

    def test_get_company_enrollment_summary_success(self):
        response = self.client.get(reverse('company_enrollment_summary_api', kwargs={'comp_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')

        summary = json.loads(response.content)
        self.assertIn('enrollmentNotComplete', summary)
        self.assertIn('enrollmentCompleted', summary)
        self.assertIn('enrollmentNotStarted', summary)
        
        not_started = summary['enrollmentNotStarted']
        self.assertEqual(len(not_started), 1)
        self.assertEqual(not_started[0]['id'], self.normalize_key(4))
        
        started = summary['enrollmentNotComplete']
        self.assertEqual(len(started), 0)

        completed = summary['enrollmentCompleted']
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0]['id'], self.normalize_key(3))
        
    def test_get_company_enrollment_summary_company_non_existent(self):

        response = self.client.get(reverse('company_enrollment_summary_api', kwargs={'comp_id': self.normalize_key(10)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
