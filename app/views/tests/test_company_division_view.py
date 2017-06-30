import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class CompanyDivisionViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['83_company_division',
                '49_period_definition', '10_company',
                '24_person', '23_auth_user']

    def test_get_company_division(self):
        response = self.client.get(reverse('company_division_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['division'], 'Boston')

    def test_get_company_division_by_company(self):
        response = self.client.get(reverse('company_division_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['company'], self.normalize_key(1))

    def test_delete_company_division(self):
        response = self.client.get(reverse('company_division_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('company_division_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_division_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_division(self):
        post_data = {
            "company": 2,
            "division": "For Test",
            "description": "For Test",
            "code": "FT"
        }

        response = self.client.post(reverse('company_division_post_api'), post_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_division_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(2))

        key = result['id']
        response = self.client.get(reverse('company_division_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(2))
        self.assertEqual(result['division'], 'For Test')
        self.assertEqual(result['description'], 'For Test')
        self.assertEqual(result['code'], 'FT')

    def test_put_company_division(self):
        put_data = {
            "id": 2,
            "company": 1,
            "division": "For Test",
            "description": "For Test",
            "code": "FT"
        }

        response = self.client.put(reverse('company_division_api',
                                            kwargs={'pk': self.normalize_key(2)}),
                                            data=json.dumps(put_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('company_division_api',
                                           kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['division'], 'For Test')
        self.assertEqual(result['description'], 'For Test')
        self.assertEqual(result['code'], 'FT')
