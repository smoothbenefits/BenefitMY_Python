import json
import sys
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class EmployeeCompensationTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person',
                '27_compensation_update_reason',
                '49_period_definition',
                '50_employee_compensation',
                '10_company',
                '23_auth_user']

    def test_get_employee_compensation_success(self):
        response = self.client.get(reverse('employee_compensation_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        employee_compensation = json.loads(response.content)
        self.assertEqual(employee_compensation['annual_base_salary'], None)
        self.assertEqual(employee_compensation['increase_percentage'], '3.50')
        self.assertEqual(employee_compensation['reason']['id'], self.normalize_key(1))

    def test_get_employee_compensation_by_person_success(self):
        response = self.client.get(reverse('employee_compensation_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        employee_compensations = json.loads(response.content)
        self.assertEqual(len(employee_compensations), 3)
        employee_compensation = employee_compensations[0]
        self.assertEqual(employee_compensation['annual_base_salary'], '100000.00')
        self.assertEqual(employee_compensation['increase_percentage'], None)

    def test_get_employee_compensation_non_exist(self):
        response = self.client.get(reverse('employee_compensation_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_compensation_non_exist_person(self):
        response = self.client.get(reverse('employee_compensation_by_person_api',
                                           kwargs={'person_id': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        compensation = json.loads(response.content)
        self.assertEqual(len(compensation), 0)

    def test_post_employee_compensation_success(self):
        post_data = {
            "person": self.normalize_key(1),
            "reason": self.normalize_key(1),
            "annual_base_salary": "40022.00",
            "effective_date": "2008-03-01T15:45:09Z",
            "increase_percentage": "50"
        }
        response = self.client.post(reverse('employee_compensation_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(6))
        self.assertEqual(result['person'], 1)
        self.assertEqual(result['reason'], 1)
        self.assertEqual(result['annual_base_salary'], "40022.00")
        self.assertEqual(result['effective_date'], "2008-03-01T15:45:09Z")
        self.assertEqual(result['increase_percentage'], "50")

        post_data = {
            "person": self.normalize_key(2),
            "reason": self.normalize_key(1),
            "projected_hour_per_month": "200.00",
            "hourly_rate": "980.01",
            "effective_date": "2008-08-01T15:45:09Z"
        }
        response = self.client.post(reverse('employee_compensation_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(7))
        self.assertEqual(result['person'], 2)
        self.assertEqual(result['reason'], 1)
        self.assertEqual(result['projected_hour_per_month'], "200.00")
        self.assertEqual(result['effective_date'], "2008-08-01T15:45:09Z")
        self.assertEqual(result['hourly_rate'], "980.01")

    def test_delete_employee_compensation_success(self):
        response = self.client.delete(reverse('employee_compensation_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

    def test_delete_employee_compensation_non_exist_failure(self):
        response = self.client.delete(reverse('employee_compensation_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
