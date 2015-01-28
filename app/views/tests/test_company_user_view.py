from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class UserCompanyTestCase(TestCase):
    fixtures = ['34_company_user', '10_company', '23_auth_user']

    def test_get_company_users(self):
        response = self.client.get(reverse('user_company_api',
                                   kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['company_roles'][0]['id'], 1)
        self.assertEqual(result['company_roles'][0]['company']['name'],
                         'BenefitMy Inc.')


class CompanyUsersTestCase(TestCase):
    fixtures = ['34_company_user', '10_company', '23_auth_user']

    def test_get_company_users(self):
        response = self.client.get(reverse('company_users_api',
                                   kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['user_roles'][0]['id'], 1)
        self.assertEqual(result['user_roles'][0]['company_user_type'], 'broker')
        self.assertEqual(result['user_roles'][0]['user']['first_name'], 'John')
        self.assertEqual(result['user_roles'][0]['user']['email'],
                         'user1@benefitmy.com')
        self.assertEqual(result['user_roles'][0]['new_employee'], True)

        self.assertEqual(result['user_roles'][3]['id'], 4)
        self.assertEqual(result['user_roles'][3]['company_user_type'], 'employee')
        self.assertEqual(result['user_roles'][3]['user']['first_name'], 'Jenn')
        self.assertEqual(result['user_roles'][3]['user']['email'],
                         'user4@benefitmy.com')
        self.assertEqual(result['user_roles'][3]['new_employee'], True)
