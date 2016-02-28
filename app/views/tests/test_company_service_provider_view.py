import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class CompanyServiceProviderViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['10_company', '73_company_service_providers', '49_period_definition']

    def test_get_company_service_provider_success(self):
        response = self.client.get(reverse('company_service_provider_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['provider_type'], 'payroll')
        self.assertEqual(result['email'], 'payroll_company_1@benefitmy.com')

    def test_create_company_service_provider_success(self):
        post_data = {'company': self.normalize_key(1),
                    'provider_type': 'payroll',
                    'email': 'testing@benefitmy.com',
                    'phone': '123456789',
                    'show_to_employee': True}
        response = self.client.post(reverse('company_service_provider_post_api'),
                                           json.dumps(post_data),
                                           content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_service_provider_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['provider_type'], 'payroll')
        self.assertEqual(result['email'], 'testing@benefitmy.com')
        self.assertEqual(result['phone'], '123456789')
        self.assertEqual(result['show_to_employee'], True)

    def test_update_company_service_provider_success(self):
        post_data = {'id': self.normalize_key(1),
                    'company': self.normalize_key(1),
                    'provider_type': 'benefits',
                    'show_to_employee': False}
        response = self.client.put(reverse('company_service_provider_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                           json.dumps(post_data),
                                           content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('company_service_provider_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['provider_type'], 'benefits')
        self.assertEqual(result['show_to_employee'], False)

    def test_get_company_service_provider_by_company_success(self):
        response = self.client.get(reverse('company_service_provider_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 3)
        result = sorted(result, key=lambda r : r['id'])
        self.assertEqual(result[0]['company'], self.normalize_key(1))
        self.assertEqual(result[0]['provider_type'], 'payroll')
        self.assertEqual(result[0]['show_to_employee'], True)
        self.assertEqual(result[0]['phone'], '1234567890')
        self.assertEqual(result[0]['email'], 'payroll_company_1@benefitmy.com')
