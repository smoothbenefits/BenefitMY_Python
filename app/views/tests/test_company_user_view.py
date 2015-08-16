from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class UserCompanyTestCase(TestCase, ViewTestBase):
    fixtures = ['34_company_user', '49_period_definition', '10_company', '23_auth_user']

    def test_get_company_users(self):
        response = self.client.get(reverse('user_company_api',
                                   kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['company_roles'][0]['id'], self.normalize_key(1))
        self.assertEqual(result['company_roles'][0]['company']['name'],
                         'BenefitMy Inc.')
        self.assertIn('pay_period_definition', result['company_roles'][0]['company'])
        self.assertEqual(result['company_roles'][0]['company']['pay_period_definition']['name'], 'Semi-Monthly')
        self.assertEqual(result['company_roles'][0]['company']['pay_period_definition']['id'], self.normalize_key(5))
        self.assertEqual(result['company_roles'][0]['company']['pay_period_definition']['month_factor'], 0.5)


class CompanyUsersTestCase(TestCase, ViewTestBase):
    fixtures = ['34_company_user', '49_period_definition', '10_company', '23_auth_user']

    def test_get_company_users(self):
        response = self.client.get(reverse('company_users_api',
                                   kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['user_roles'][0]['id'], self.normalize_key(1))
        self.assertEqual(result['user_roles'][0]['company_user_type'], 'broker')
        self.assertEqual(result['user_roles'][0]['user']['first_name'], 'John')
        self.assertEqual(result['user_roles'][0]['user']['email'],
                         'user1@benefitmy.com')
        self.assertEqual(result['user_roles'][0]['new_employee'], True)

        self.assertEqual(result['user_roles'][3]['id'], self.normalize_key(4))
        self.assertEqual(result['user_roles'][3]['company_user_type'], 'employee')
        self.assertEqual(result['user_roles'][3]['user']['first_name'], 'Jenn')
        self.assertEqual(result['user_roles'][3]['user']['email'],
                         'user4@benefitmy.com')
        self.assertEqual(result['user_roles'][3]['new_employee'], True)


    def test_get_company_employee_count(self):
        response = self.client.get(reverse('company_employee_count',
                                   kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['employees_count'], 2)

        response = self.client.get(reverse('company_employee_count',
                                   kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['employees_count'], 0)


    def test_get_company_broker_count(self):
        response = self.client.get(reverse('company_broker_count',
                                   kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['brokers_count'], 1)

        response = self.client.get(reverse('company_broker_count',
                                   kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['brokers_count'], 0)


    def test_get_broker_company_count(self):
        response = self.client.get(reverse('broker_company_count',
                                   kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['companies_count'], 1)

        response = self.client.get(reverse('broker_company_count',
                                   kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['companies_count'], 0)
