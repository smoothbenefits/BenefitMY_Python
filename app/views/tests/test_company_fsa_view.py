from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class FsaTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['37_fsa', '23_auth_user', '24_person', '10_company', '42_company_fsa']

    def test_get_company_fsa(self):
        response = self.client.get(reverse('company_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['fsa_plan']['id'], self.normalize_key(2))

    # def test_delete_company_fsa(self):
    #     response = self.client.get(reverse('company_fsa_api',
    #                                        kwargs={'pk': self.normalize_key(1)}))
    #     self.assertIsNotNone(response)
    #     self.assertEqual(response.status_code, 200)

    #     result = json.loads(response.content)
    #     self.assertEqual(type(result), list)
    #     self.assertTrue(len(result) > 0)
    #     self.assertEqual(type(result[0]), dict)
    #     self.assertEqual(result[0]['fsa_plan']['id'], self.normalize_key(2))

    #     response = self.client.delete(reverse('company_fsa_api',
    #                                           kwargs={'pk': self.normalize_key(1)}))

    #     self.assertEqual(response.status_code, 204)
    #     response = self.client.get(reverse('company_fsa_api',
    #                                        kwargs={'pk': self.normalize_key(1)}))
    #     self.assertIsNotNone(response)
    #     self.assertEqual(response.status_code, 404)
    #     result = json.loads(response.content)
    #     self.assertEqual(result['detail'], 'Not found')

    # def test_post_company_fsa(self):
    #     company_fsa_data = [{"company_id": 3,
    #                "fsa_plan_id": 3}]

    #     response = self.client.post(reverse('company_fsa_api', kwargs={'pk': self.normalize_key(3)}),
    #                                 company_fsa_data)
    #     self.assertIsNotNone(response)
    #     self.assertEqual(response.status_code, 201)
    #     response = self.client.get(reverse('company_fsa_api',
    #                                        kwargs={'pk': self.normalize_key(4)}))
    #     self.assertIsNotNone(response)
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.content)
    #     self.assertEqual(type(result), list)
    #     self.assertTrue(len(result) > 0)
    #     self.assertEqual(type(result[0]), dict)
    #     self.assertEqual(result[0]['company'], self.normalize_key(3))
    #     self.assertEqual(result[0]['fsa_plan']['id'], self.normalize_key(3))

