import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class CompanyCommuterPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['53_company_commuter_plan', '54_person_company_commuter_plan', 
                '49_period_definition', '10_company', '24_person', '23_auth_user']

    def test_get_company_commuter_plan(self):
        response = self.client.get(reverse('company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['plan_name'], 'Commuter Basic')
        self.assertEqual(result['enable_transit_benefit'], True)
        self.assertEqual(result['enable_parking_benefit'], True)
        self.assertEqual(float(result['employer_transit_contribution']), 50.50)
        self.assertEqual(float(result['employer_parking_contribution']), 10.23)
        self.assertEqual(result['deduction_period'], 'PerPayPeriod')

    def test_get_company_commuter_plan_by_company(self):
        response = self.client.get(reverse('company_commuter_plan_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['company'], self.normalize_key(1))
        self.assertEqual(result[0]['plan_name'], 'Commuter Basic')
        self.assertEqual(result[0]['enable_transit_benefit'], True)
        self.assertEqual(result[0]['enable_parking_benefit'], True)
        self.assertEqual(float(result[0]['employer_transit_contribution']), 50.50)
        self.assertEqual(float(result[0]['employer_parking_contribution']), 10.23)
        self.assertEqual(result[0]['deduction_period'], 'PerPayPeriod')

    def test_delete_company_commuter_plan(self):
        response = self.client.get(reverse('company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('company_commuter_plan_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_commuter_plan(self):
        post_data = {"company": 2,
                     "plan_name": "Test Commuter",
                     "enable_transit_benefit": True,
                     "enable_parking_benefit": False,
                     "employer_transit_contribution": 0.0,
                     "employer_parking_contribution": 1.0,
                     "deduction_period": "Monthly"}
        response = self.client.post(reverse('company_commuter_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            post_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(2))

        key = result['id']
        response = self.client.get(reverse('company_commuter_plan_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(2))
        self.assertEqual(result['plan_name'], 'Test Commuter')
        self.assertEqual(result['enable_transit_benefit'], True)
        self.assertEqual(result['enable_parking_benefit'], False)
        self.assertEqual(float(result['employer_transit_contribution']), 0.0)
        self.assertEqual(float(result['employer_parking_contribution']), 1.0)
        self.assertEqual(result['deduction_period'], 'Monthly')
