import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class CompanyLtdInsuranceTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['ltd_insurance', '23_auth_user',
                '49_period_definition', '10_company']

    def test_get_company_ltd_insurance_success(self):
        response = self.client.get(reverse('company_ltd_insurance_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 2)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(len(result['age_based_rates']), 0)


    def test_get_company_ltd_insurance_invalid_company(self):
        response = self.client.get(reverse('company_ltd_insurance_plan_api',
                                           kwargs={'pk': self.normalize_key(100)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(len(array), 0)


    def test_post_company_ltd_insurance_success(self):
        std_data = {'company': self.normalize_key(3),
                    'ltd_insurance_plan': self.normalize_key(1),
                    'elimination_period_in_months': 2, 
                    'duration': 21, 
                    'percentage_of_salary': '80.00', 
                    'max_benefit_monthly': '3344.00', 
                    'rate': '0.220000', 
                    'age_based_rates': [], 
                    'employer_contribution_percentage': '22.00', 
                    'paid_by': None}
        response = self.client.post(reverse('company_ltd_insurance_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            json.dumps(std_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_ltd_insurance_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 1)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(3))
        self.assertEqual(len(result['age_based_rates']), 0)
        self.assertEqual(result['rate'], '0.220000')
        self.assertEqual(result['duration'], 21)
        self.assertEqual(result['elimination_period_in_months'], 2)
        self.assertEqual(result['max_benefit_monthly'], '3344.00')
        self.assertEqual(result['percentage_of_salary'], '80.00')
        self.assertEqual(result['employer_contribution_percentage'], '22.00')

    def test_post_company_ltd_insurance_age_based_rates_success(self):
        std_data = {'company': self.normalize_key(3),
                    'ltd_insurance_plan': self.normalize_key(1),
                    'elimination_period_in_months': 3, 
                    'duration': 90, 
                    'percentage_of_salary': '80.00', 
                    'max_benefit_monthly': '6677.00', 
                    'rate': None,
                    'age_based_rates': [{
                        'age_min': 20,
                        'age_max': 30,
                        'rate': '32.0000'
                    }, {
                        'age_min': 30,
                        'age_max': 40,
                        'rate': '33.0000'
                    }, {
                        'age_min': 40,
                        'age_max': 50,
                        'rate': '34.0000'
                    }], 
                    'employer_contribution_percentage': '22.00', 
                    'paid_by': None}
        response = self.client.post(reverse('company_ltd_insurance_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            json.dumps(std_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_ltd_insurance_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 1)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(3))
        self.assertEqual(len(result['age_based_rates']), 3)
        self.assertEqual(result['rate'], None)
        self.assertEqual(result['duration'], 90)
        self.assertEqual(result['elimination_period_in_months'], 3)
        self.assertEqual(result['max_benefit_monthly'], '6677.00')
        self.assertEqual(result['percentage_of_salary'], '80.00')
        self.assertEqual(result['employer_contribution_percentage'], '22.00')

