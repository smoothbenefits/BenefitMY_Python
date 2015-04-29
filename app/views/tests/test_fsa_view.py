from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class FsaTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['fsa', '23_auth_user', '24_person', '10_company']

    def test_get_fsa(self):
        response = self.client.get(reverse('user_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['primary_amount_per_year'], '2500.00')
        self.assertEqual(result['dependent_amount_per_year'], '2500.00')
        self.assertEqual(result['broker_user'], self.normalize_key(1))
        self.assertEqual(result['update_reason'], 'new enroll')

    def test_delete_fsa(self):
        response = self.client.get(reverse('fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['primary_amount_per_year'], '2500.00')
        self.assertEqual(result['dependent_amount_per_year'], '2500.00')
        self.assertEqual(result['broker_user'], self.normalize_key(1))
        self.assertEqual(result['update_reason'], 'new enroll')

        response = self.client.delete(reverse('fsa_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_fsa(self):
        dd_data = {"primary_amount_per_year": "500.00",
                   "dependent_amount_per_year": "500.00",
                   "user": 4,
                   "update_reason": "new enroll"}

        response = self.client.post(reverse('fsa_api', kwargs={'pk': self.normalize_key(4)}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('fsa_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['primary_amount_per_year'], '500.00')
        self.assertEqual(result['dependent_amount_per_year'], '500.00')
        self.assertEqual(result['user'], self.normalize_key(4))
        self.assertEqual(result['update_reason'], 'new enroll')

        #Test post duplicate data
        response = self.client.post(reverse('fsa_api', kwargs={'pk': self.normalize_key(4)}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 409)
