import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class PersonEnrollmentSummaryTestCase(TestCase, ViewTestBase):
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

    def test_get_person_enrollment_summary(self):
        response = self.client.get(reverse('person_benefit_summary_api', kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')

        summary = json.loads(response.content)
        self.assertIn('person', summary)
        self.assertIn('health_benefit_enrolled', summary)
        self.assertIn('health_benefit_waived', summary)
        self.assertIn('hra', summary)
        self.assertIn('fsa', summary)
        self.assertIn('basic_life', summary)
        self.assertIn('supplemental_life', summary)
        self.assertIn('std', summary)
        self.assertIn('ltd', summary)

        self.assertTrue(len(summary['health_benefit_enrolled']) > 0)
        self.assertTrue(len(summary['health_benefit_waived']) == 0)
        self.assertTrue(len(summary['hra']) > 0)
        self.assertTrue(len(summary['basic_life']) > 0)
        self.assertTrue(len(summary['supplemental_life']) > 0)
        self.assertTrue(len(summary['std']) > 0)
        self.assertTrue(len(summary['ltd']) > 0)
        self.assertTrue(len(summary['fsa']) > 0)

    def test_get_person_enrollment_summary_not_enrolled(self):
        response = self.client.get(reverse('person_benefit_summary_api', kwargs={'person_id': self.normalize_key(5)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')

        summary = json.loads(response.content)
        self.assertIn('person', summary)
        self.assertIn('health_benefit_enrolled', summary)
        self.assertIn('health_benefit_waived', summary)
        self.assertIn('hra', summary)
        self.assertIn('fsa', summary)
        self.assertIn('basic_life', summary)
        self.assertIn('supplemental_life', summary)
        self.assertIn('std', summary)
        self.assertIn('ltd', summary)

        self.assertEqual(len(summary['health_benefit_enrolled']), 0)
        self.assertEqual(len(summary['health_benefit_waived']), 0)
        self.assertEqual(len(summary['hra']), 0)
        self.assertEqual(len(summary['basic_life']), 0)
        self.assertEqual(len(summary['supplemental_life']), 0)
        self.assertEqual(len(summary['std']), 0)
        self.assertEqual(len(summary['ltd']), 0)
        self.assertEqual(len(summary['fsa']), 0)

    def test_get_person_enrollment_summary_not_exist(self):
        response = self.client.get(reverse('person_benefit_summary_api', kwargs={'person_id': self.normalize_key(100)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
