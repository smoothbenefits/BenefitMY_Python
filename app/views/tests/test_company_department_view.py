import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class CompanyDepartmentViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['79_company_department',
                '49_period_definition', '10_company',
                '24_person', '23_auth_user']

    def test_get_company_department(self):
        response = self.client.get(reverse('company_department_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['department'], 'Human Resources')

    def test_get_company_department_by_company(self):
        response = self.client.get(reverse('company_department_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 3)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['company'], self.normalize_key(1))

    def test_delete_company_department(self):
        response = self.client.get(reverse('company_department_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('company_department_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_department_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_department(self):
        post_data = {
            "company": 2,
            "department": "For Test",
            "description": "For Test"
        }

        response = self.client.post(reverse('company_department_post_api'), post_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_department_api',
                                           kwargs={'pk': self.normalize_key(4)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(2))

        key = result['id']
        response = self.client.get(reverse('company_department_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(2))
        self.assertEqual(result['department'], 'For Test')
        self.assertEqual(result['description'], 'For Test')

    def test_put_company_department(self):
        put_data = {
            "id": 2,
            "company": 1,
            "department": "For Test",
            "description": "For Test"
        }

        response = self.client.put(reverse('company_department_api',
                                            kwargs={'pk': self.normalize_key(2)}),
                                            data=json.dumps(put_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('company_department_api',
                                           kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['department'], 'For Test')
        self.assertEqual(result['description'], 'For Test')
