import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class CompanyHraPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['46_hra_plan', '47_company_hra_plan', '48_person_company_hra_plan', '10_company',
    '24_person', '23_auth_user']

    def test_get_company_hra_plan(self):
        response = self.client.get(reverse('company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['hra_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['cost_per_month'], '300.45')

    def test_get_company_hra_plan_by_company(self):
        response = self.client.get(reverse('company_hra_plan_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['company'], self.normalize_key(1))
        self.assertEqual(result[0]['hra_plan']['id'], self.normalize_key(1))
        self.assertEqual(result[0]['cost_per_month'], '300.45')

    def test_delete_company_hra_plan(self):
        response = self.client.get(reverse('company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('company_hra_plan_api', 
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_hra_plan(self):
        post_data = {"company": 2,
                     "hra_plan": 2}
        response = self.client.post(reverse('company_hra_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            post_data)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(2))

        key = result['id']
        response = self.client.get(reverse('company_hra_plan_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(2))


