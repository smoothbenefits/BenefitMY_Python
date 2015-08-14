import json
import sys
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class EmployeeTimeTrackingTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person',
                '10_company',
                '49_period_definition',
                '51_employee_timetracking',
                '23_auth_user',
                '11_address',
                '12_phone']

    def test_get_employee_timetracking_success(self):
        response = self.client.get(reverse('employee_timetracking_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        employee_timetracking = json.loads(response.content)
        self.assertEqual(employee_timetracking['actual_hour'], '180.0000')
        self.assertEqual(employee_timetracking['projected_hour'], '160.0000')
        self.assertEqual(employee_timetracking['company'], self.normalize_key(1))
        self.assertEqual(employee_timetracking['person'], self.normalize_key(3))

    def test_get_employee_timetracking_by_person_success(self):
        response = self.client.get(reverse('employee_timetracking_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        employee_timetrackings = json.loads(response.content)
        self.assertEqual(len(employee_timetrackings), 1)
        employee_timetracking = employee_timetrackings[0]
        self.assertEqual(employee_timetracking['actual_hour'], '180.0000')
        self.assertEqual(employee_timetracking['projected_hour'], '160.0000')
        self.assertEqual(employee_timetracking['company'], self.normalize_key(1))
        self.assertEqual(employee_timetracking['person'], self.normalize_key(3))

    def test_get_employee_timetracking_non_exist(self):
        response = self.client.get(reverse('employee_timetracking_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_timetracking_non_exist_person(self):
        response = self.client.get(reverse('employee_timetracking_by_person_api',
                                           kwargs={'person_id': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        timetracking = json.loads(response.content)
        self.assertEqual(len(timetracking), 0)

    def test_post_employee_timetracking_success(self):
        post_data = {
            "person": self.normalize_key(1),
            "company": self.normalize_key(1),
            "projected_hour": "90",
            "actual_hour": "80",
            "start_date": "2015-08-01",
            "end_date": "2015-08-31"
        }
        response = self.client.post(reverse('employee_timetracking_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(2))
        self.assertEqual(result['person'], 1)
        self.assertEqual(result['company'], 1)
        self.assertEqual(result['projected_hour'], "90")
        self.assertEqual(result['actual_hour'], "80")
        self.assertEqual(result['start_date'], "2015-08-01")
        self.assertEqual(result['end_date'], "2015-08-31")

    def test_delete_employee_timetracking_non_exist_failure(self):
        response = self.client.delete(reverse('employee_timetracking_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
