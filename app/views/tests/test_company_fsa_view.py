from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class CompanyFsaTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['37_fsa_plan', '23_auth_user', '24_person', '10_company', '42_company_fsa']

    def test_get_company_fsa_by_company(self):
        response = self.client.get(reverse('company_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['fsa_plan']['id'], self.normalize_key(2))

    def test_get_company_fsa(self):
        response = self.client.get(reverse('broker_company_fsa_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(2))
        self.assertEqual(result['fsa_plan']['id'], self.normalize_key(3))

    def test_delete_company_fsa(self):
        response = self.client.get(reverse('broker_company_fsa_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('broker_company_fsa_api',
                                              kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('broker_company_fsa_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_fsa(self):
        fsa_data = {"company": 3,
                    "fsa_plan": 3}
        response = self.client.post(reverse('broker_company_fsa_api',
                                            kwargs={'pk': self.normalize_key(2)}),
                                            fsa_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('broker_company_fsa_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(3))

        key = result['id']
        response = self.client.get(reverse('broker_company_fsa_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(3))
