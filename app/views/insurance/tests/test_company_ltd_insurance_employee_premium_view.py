import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class CompanyLtdInsuranceEmployeePremiumViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', '24_person', 'ltd_insurance',
    '27_compensation_update_reason', '50_employee_compensation', '49_period_definition', '10_company',
    'employee_profile']

    def test_get_company_ltd_insurance_employee_premium_view_success(self):
        response = self.client.get(reverse('user_company_ltd_insurance_premium_api',
                                           kwargs={'pk': self.normalize_key(2),
                                                   'user_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertIn('total', result)
        self.assertIn('employee', result)

        self.assertEqual(result['total'], 241.5)
        self.assertEqual(result['employee'], 48.3)

    def test_get_company_ltd_insurance_employee_premium_view_no_salary(self):

        response = self.client.get(reverse('user_company_ltd_insurance_premium_api',
                                           kwargs={'pk': self.normalize_key(1),
                                                   'user_id': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertIn('message', result)
        self.assertEqual(result['message'], 'No salary info')

    def test_get_company_ltd_insurance_employee_premium_view_no_ltd_plan(self):
        response = self.client.get(reverse('user_company_ltd_insurance_premium_api',
                                   kwargs={'pk': self.normalize_key(60),
                                           'user_id': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
