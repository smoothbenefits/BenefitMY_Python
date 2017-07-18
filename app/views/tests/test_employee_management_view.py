import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class EmployeeManagementTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person',
                '79_company_department', '82_company_job', '83_company_division',
                'employee_profile',
                '49_period_definition',
                '10_company',
                '23_auth_user',
                '11_address',
                '12_phone']

    def test_terminate_employee_success(self):
        post_data = {"person_id": 3,
                     "company_id": 1,
                     "end_date": '2010-06-01'}

        post_response = self.client.post(reverse('employee_management_termination_api',
                                           kwargs={'company_id': self.normalize_key(1)}),
                                         data=json.dumps(post_data),
                                         content_type='application/json')

        self.assertIsNotNone(post_response)
        self.assertEqual(post_response.status_code, 200)
        post_result = json.loads(post_response.content)
        self.assertIn('output_data', post_result)
        self.assertEqual(post_result['output_data']['id'], self.normalize_key(1))
        self.assertEqual(post_result['output_data']['person'], self.normalize_key(3))
        self.assertEqual(post_result['output_data']['company'], self.normalize_key(1))
        self.assertEqual(post_result['output_data']['end_date'], "2010-06-01")
        self.assertEqual(post_result['output_data']['employment_status'], "Terminated")

        get_response = self.client.get(reverse('employee_profile_by_person_company_api',
                                           kwargs={
                                            'person_id': self.normalize_key(3),
                                            'company_id': self.normalize_key(1)
                                            }))

        self.assertIsNotNone(get_response)
        self.assertEqual(get_response.status_code, 200)

        get_result = json.loads(get_response.content)
        self.assertIn('id', get_result)
        self.assertEqual(get_result['id'], self.normalize_key(1))
        self.assertEqual(get_result['person'], self.normalize_key(3))
        self.assertEqual(get_result['company'], self.normalize_key(1))
        self.assertEqual(get_result['end_date'], "2010-06-01")
        self.assertEqual(get_result['employment_status'], "Terminated")
