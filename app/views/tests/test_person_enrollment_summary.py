import json
import sys
import copy
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class PersonEnrollmentSummaryTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person', '10_company', '23_auth_user',
                '17_supplemental_life_insurance_condition',
                '21_benefit_plan', '22_benefit_details', '26_supplemental_life_insurance',
                '31_company_benefit_plan_option', '32_enrolled', '34_company_user',
                '37_fsa_plan', '38_supplemental_life_rate', '39_company_supplement_life_insurance',
                '41_user_company_benefit_plan_option', '42_company_fsa', '43_fsa',
                '44_person_company_suppl_life', '45_suppl_life_beneficiary', '46_hra_plan',
                '47_company_hra_plan', '48_person_company_hra_plan', 'company_features',
                'life_insurance', 'ltd_insurance', 'std_insurance', 'waived_benefits']

    def test_get_person_enrollment_summary(self):
        response = self.client.get(reverse('person_benefit_summary_api', kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '')
        summary = json.loads(response.content)
        print summary
