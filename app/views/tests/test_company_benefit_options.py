from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class CompanyBenefitPlanOptionTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['15_benefit_policy_key', '23_auth_user', '24_person', '10_company', 
                '16_benefit_policy_type', '21_benefit_plan', '22_benefit_details', 
                '13_benefit_type', '31_company_benefit_plan_option']

    def test_get_company_benefit_plan_by_company(self):
        response = self.client.get(reverse('company_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(type(result['benefits']), list)
        self.assertTrue(len(result['benefits']) > 0)


    def test_post_company_benefit_plan_option(self):
        benefit_data = {"company": self.normalize_key(1),
                        "benefit": {
                            "benefit_option_type": "individual_plus_one",
                            "total_cost_per_period": 100.00,
                            "employee_cost_per_period": 50.00,
                            "benefit_plan_id": self.normalize_key(1),
                        }}
        response = self.client.post(reverse('company_benefit_post_api'), 
                                    data=json.dumps(benefit_data),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
