from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class FsaTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['37_fsa_plan', '23_auth_user', '24_person', '49_period_definition', '10_company']

    def test_get_fsa(self):
        response = self.client.get(reverse('broker_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['broker_user'], self.normalize_key(1))
        self.assertEqual(result['name'], 'WageWork FSA')

    def test_delete_fsa(self):
        response = self.client.get(reverse('broker_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['broker_user'], self.normalize_key(1))
        self.assertEqual(result['name'], 'WageWork FSA')

        response = self.client.delete(reverse('broker_fsa_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('broker_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_fsa(self):
        dd_data = {"name": "New FSA",
                   "broker_user": 4}

        response = self.client.post(reverse('broker_fsa_api', kwargs={'pk': self.normalize_key(4)}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('broker_fsa_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['broker_user'], self.normalize_key(4))
        self.assertEqual(result['name'], 'New FSA')
