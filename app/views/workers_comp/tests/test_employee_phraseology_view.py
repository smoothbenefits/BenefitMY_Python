import json
from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class EmployeePhraseologyViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['74_phraseology', '75_company_phraseology',
                '76_employee_phraseology', '49_period_definition',
                '10_company', '24_person', '23_auth_user']

    def test_get_employee_phraseology(self):
        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['employee_person'], self.normalize_key(3))
        self.assertEqual(result['phraseology']['id'], self.normalize_key(5))

    def test_get_employee_phraseology_by_employee_person(self):
        response = self.client.get(reverse('employee_phraseology_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['employee_person'], self.normalize_key(3))

    def test_delete_employee_phraseology(self):
        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('employee_phraseology_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_employee_phraseology_none_exist(self):
        post_data = {
            "employee_person": 2,
            "phraseology": 6
        }

        response = self.client.post(reverse('employee_phraseology_post_api'), post_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': self.normalize_key(4)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['employee_person'], self.normalize_key(2))

        key = result['id']
        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['employee_person'], self.normalize_key(2))
        self.assertEqual(result['phraseology']['id'], self.normalize_key(6))
        self.assertEqual(result['start_date'], date.today().isoformat())
        self.assertIsNone(result['end_date'])

    def test_post_employee_phraseology_exist_current(self):
        post_data = {
            "employee_person": 3,
            "phraseology": 8
        }

        response = self.client.post(reverse('employee_phraseology_post_api'), post_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': self.normalize_key(4)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['employee_person'], self.normalize_key(3))

        key = result['id']
        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['employee_person'], self.normalize_key(3))
        self.assertEqual(result['phraseology']['id'], self.normalize_key(8))
        self.assertEqual(result['start_date'], date.today().isoformat())
        self.assertIsNone(result['end_date'])

        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['employee_person'], self.normalize_key(3))
        self.assertEqual(result['phraseology']['id'], self.normalize_key(7))
        self.assertEqual(result['start_date'], '2015-11-27')
        self.assertEqual(result['end_date'], date.today().isoformat())

    def test_put_employee_phraseology(self):
        put_data = {
            "id": 2,
            "employee_person": 3,
            "phraseology": 6
        }

        response = self.client.put(reverse('employee_phraseology_api',
                                            kwargs={'pk': self.normalize_key(2)}),
                                            data=json.dumps(put_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('employee_phraseology_api',
                                           kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['employee_person'], self.normalize_key(3))
        self.assertEqual(result['phraseology']['id'], self.normalize_key(6))
        self.assertEqual(result['start_date'], '2015-11-27')
        self.assertIsNone(result['end_date'])
