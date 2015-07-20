import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class HraPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['46_hra_plan', '47_company_hra_plan', '48_person_company_hra_plan', '10_company',
    '24_person', '23_auth_user']

    def test_get_hra_plan(self):
        response = self.client.get(reverse('hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['name'], "HRA Basic")

    def test_delete_hra_plan(self):
        response = self.client.get(reverse('hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('hra_plan_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_hra_plan(self):
        post_data = {"name": "Test HRA Plan",
                     "description": "Test HRA Plan Description"}
        response = self.client.post(reverse('hra_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            data=json.dumps(post_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('hra_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['name'], "Test HRA Plan")

        key = result['id']
        response = self.client.get(reverse('hra_plan_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['name'], "Test HRA Plan")
        self.assertEqual(result['description'], "Test HRA Plan Description")

    def test_put_hra_plan(self):
        put_data = {
          "name": "Test HRA Plan",
          "description": "Test HRA Plan Description Updated"}
        response = self.client.put(reverse('hra_plan_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                            data=json.dumps(put_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['name'], "Test HRA Plan")
        self.assertEqual(result['description'], "Test HRA Plan Description Updated")
