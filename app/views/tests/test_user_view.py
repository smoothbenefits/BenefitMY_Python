from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class UserTestCase(TestCase):
    # your fixture files here
    fixtures = ['24_person', '10_company', '23_auth_user', '11_address',
                '12_phone']

    def test_get_user(self):
        response = self.client.get(reverse('user_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['user']['first_name'], 'John')
        self.assertEqual(result['user']['last_name'], 'Hancock')
        self.assertEqual(result['user']['id'], 1)
        self.assertEqual(result['user']['email'], 'user1@benefitmy.com')

        response = self.client.get(reverse('user_api',
                                           kwargs={'pk': 2}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['user']['first_name'], 'Francis')
        self.assertEqual(result['user']['last_name'], 'McLaurren')
        self.assertEqual(result['user']['id'], 2)
        self.assertEqual(result['user']['email'], 'user2@benefitmy.com')


    def test_get_users(self):
        response = self.client.get(reverse('users_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)

        self.assertEqual(type(result), dict)
        self.assertEqual(type(result['users']), list)
        self.assertEqual(result['users'][0]['first_name'], 'John')
        self.assertEqual(result['users'][0]['last_name'], 'Hancock')
        self.assertEqual(result['users'][0]['id'], 1)
        self.assertEqual(result['users'][0]['email'], 'user1@benefitmy.com')

        self.assertEqual(result['users'][1]['first_name'], 'Francis')
        self.assertEqual(result['users'][1]['last_name'], 'McLaurren')
        self.assertEqual(result['users'][1]['id'], 2)
        self.assertEqual(result['users'][1]['email'], 'user2@benefitmy.com')
