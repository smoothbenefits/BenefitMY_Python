from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import MULTIPART_CONTENT
from view_test_base import ViewTestBase
import json


class CompanyGroupTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['49_period_definition', '10_company', '61_company_group', '23_auth_user']

    def test_get_company_group(self):
        response = self.client.get(reverse('company_group_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(3, len(result))

        result = sorted(result, key=lambda x: x['id'])
        self.assertEqual(result[0]['name'], "Management")
        self.assertEqual(result[0]['company']['id'], self.normalize_key(1))
        self.assertEqual(result[1]['name'], "Salary-based")
        self.assertEqual(result[1]['company']['id'], self.normalize_key(1))
        self.assertEqual(result[2]['name'], "Contractor")
        self.assertEqual(result[2]['company']['id'], self.normalize_key(1))

    def test_post_company_group(self):
        post_data = {
            "name": "For Testing",
            "company": self.normalize_key(2)
        }
        response = self.client.post(reverse('company_group_api',
                                    kwargs={'pk': self.normalize_key(1)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(4))
        self.assertEqual(result['name'], 'For Testing')
        self.assertEqual(result['company'], 2)

    def test_put_company_group(self):
        post_data = {
            "id": self.normalize_key(1),
            "name": "For Testing",
            "company": self.normalize_key(2)
        }
        response = self.client.put(reverse('company_group_api',
                                    kwargs={'pk': self.normalize_key(1)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(1))
        self.assertEqual(result['name'], 'For Testing')
        self.assertEqual(result['company'], self.normalize_key(2))

    def test_delete_company_group(self):
        response = self.client.delete(reverse('company_group_api',
                                    kwargs={'pk': self.normalize_key(1)}),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_group_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(2, len(result))
