from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class UserCompanyTestCase(TestCase):
    # your fixture files here
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
