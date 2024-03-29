import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class CompanyStdInsuranceEmployeePremiumViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', '24_person', 'std_insurance',
    '27_compensation_update_reason', '50_employee_compensation', '49_period_definition', '10_company',
    '79_company_department', '82_company_job', '83_company_division',
    'employee_profile']

    def test_get_company_std_insurance_employee_premium_view_success(self):
        body = {'amount': 100000}
        response = self.client.post(reverse('user_company_std_insurance_premium_api',
                                            kwargs={'pk': self.normalize_key(2),
                                                    'user_id': self.normalize_key(3)}),
                                    json.dumps(body),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertIn('total', result)
        self.assertIn('employee', result)

        self.assertEqual(result['total'], 7.961538461538462)
        self.assertEqual(result['employee'], 1.5923076923076922)

    def test_get_company_std_insurance_employee_premium_view_no_salary(self):
        body = {'amount': 0}
        response = self.client.post(reverse('user_company_std_insurance_premium_api',
                                            kwargs={'pk': self.normalize_key(1),
                                                    'user_id': self.normalize_key(1)}),
                                    json.dumps(body),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(float(result['employee']), 0)
        self.assertEqual(float(result['total']), 0)
        self.assertEqual(float(result['amount']), 0)

    def test_get_company_std_insurance_employee_premium_view_no_ltd_plan(self):
        body = {'amount': 0}
        response = self.client.post(reverse('user_company_std_insurance_premium_api',
                                    kwargs={'pk': self.normalize_key(60),
                                            'user_id': self.normalize_key(1)}),
                                    json.dumps(body),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
