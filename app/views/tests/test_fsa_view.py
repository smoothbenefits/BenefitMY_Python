from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class FsaTestCase(TestCase):
    # your fixture files here
    fixtures = ['fsa', '23_auth_user', '24_person', '10_company']

    def test_get_fsa(self):
        response = self.client.get(reverse('fsa_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)

        self.assertEqual(result[0]['amount_per_year'], '2500.00')
        self.assertEqual(result[0]['user'], 1)
        self.assertEqual(result[0]['person'], 2)
        self.assertEqual(result[0]['update_reason'], 'new enroll')

        self.assertEqual(result[1]['amount_per_year'], '2500.00')
        self.assertEqual(result[1]['user'], 1)
        self.assertEqual(result[1]['person'], 1)
        self.assertEqual(result[1]['update_reason'], 'new enroll')


    def test_delete_fsa(self):
        response = self.client.get(reverse('fsa_api',
                                           kwargs={'pk': 2}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)

        self.assertEqual(result[0]['amount_per_year'], '2500.00')
        self.assertEqual(result[0]['user'], 2)
        self.assertEqual(result[0]['person'], 3)
        self.assertEqual(result[0]['update_reason'], 'new enroll')

        response = self.client.delete(reverse('fsa_api',
                                              kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_fsa(self):
        dd_data = {"amount_per_year": "2500.00",
                   "user": 3,
                   "person": 4,
                   "update_reason": "new enroll"}

        response = self.client.post(reverse('fsa_api', kwargs={'pk': 4}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('fsa_api',
                                           kwargs={'pk': 3}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)

        self.assertEqual(result[0]['amount_per_year'], '2500.00')
        self.assertEqual(result[0]['user'], 3)
        self.assertEqual(result[0]['person'], 4)
        self.assertEqual(result[0]['update_reason'], 'new enroll')

        #Test post duplicate data
        response = self.client.post(reverse('fsa_api', kwargs={'pk': 4}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 409)
