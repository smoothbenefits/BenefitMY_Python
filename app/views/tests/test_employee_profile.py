import json
import sys
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class EmployeeProfileTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person',
                '79_company_department', '82_company_job', '83_company_division',
                'employee_profile',
                '49_period_definition',
                '10_company',
                '23_auth_user',
                '11_address',
                '12_phone']

    def test_get_employee_profile_success(self):
        response = self.client.get(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        employee_profile = json.loads(response.content)
        self.assertEqual(employee_profile['job_title'], 'Senior Software Engineer')
        self.assertEqual(employee_profile['annual_base_salary'], '140000.00')
        self.assertEqual(employee_profile['start_date'], '2010-06-01')
        self.assertEqual(employee_profile['benefit_start_date'], '2010-06-01')
        self.assertEqual(employee_profile['end_date'], None)
        self.assertEqual(employee_profile['employment_type'], 'FullTime')
        self.assertEqual(employee_profile['employment_status'], 'Active')
        self.assertEqual(employee_profile['person'], self.normalize_key(3))
        self.assertEqual(employee_profile['company'], self.normalize_key(1))
        self.assertIsNotNone(employee_profile['manager'])
        manager = employee_profile['manager']
        self.assertEqual(manager['id'], self.normalize_key(3))
        self.assertEqual(manager['first_name'], 'Lebron')
        self.assertEqual(manager['last_name'], 'James')

    def test_get_employee_profile_by_person_company_success(self):
        response = self.client.get(reverse('employee_profile_by_person_company_api',
                                           kwargs={'person_id': self.normalize_key(3),
                                                    'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        employee_profile = json.loads(response.content)
        self.assertEqual(employee_profile['job_title'], 'Senior Software Engineer')
        self.assertEqual(employee_profile['annual_base_salary'], '140000.00')
        self.assertEqual(employee_profile['start_date'], '2010-06-01')
        self.assertEqual(employee_profile['benefit_start_date'], '2010-06-01')
        self.assertEqual(employee_profile['end_date'], None)
        self.assertEqual(employee_profile['employment_type'], 'FullTime')
        self.assertEqual(employee_profile['employment_status'], 'Active')
        self.assertEqual(employee_profile['person'], self.normalize_key(3))
        self.assertEqual(employee_profile['company'], self.normalize_key(1))
        self.assertIsNotNone(employee_profile['manager'])
        manager = employee_profile['manager']
        self.assertEqual(manager['id'], self.normalize_key(3))
        self.assertEqual(manager['first_name'], 'Lebron')
        self.assertEqual(manager['last_name'], 'James')

    def test_get_employee_profile_by_company_user_success(self):
        response = self.client.get(reverse('employee_profile_by_company_user_api',
                                           kwargs={'user_id': self.normalize_key(3),
                                                    'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        employee_profile = json.loads(response.content)
        self.assertEqual(employee_profile['job_title'], 'Senior Software Engineer')
        self.assertEqual(employee_profile['annual_base_salary'], '140000.00')
        self.assertEqual(employee_profile['start_date'], '2010-06-01')
        self.assertEqual(employee_profile['benefit_start_date'], '2010-06-01')
        self.assertEqual(employee_profile['end_date'], None)
        self.assertEqual(employee_profile['employment_type'], 'FullTime')
        self.assertEqual(employee_profile['employment_status'], 'Active')
        self.assertEqual(employee_profile['person'], self.normalize_key(3))
        self.assertEqual(employee_profile['company'], self.normalize_key(1))
        self.assertIsNotNone(employee_profile['manager'])
        manager = employee_profile['manager']
        self.assertEqual(manager['id'], self.normalize_key(3))
        self.assertEqual(manager['first_name'], 'Lebron')
        self.assertEqual(manager['last_name'], 'James')

    def test_get_employee_profile_non_exist(self):
        response = self.client.get(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_profile_non_exist_person(self):
        response = self.client.get(reverse('employee_profile_by_person_company_api',
                                           kwargs={'person_id': self.normalize_key(sys.maxint),
                                                    'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_profile_non_exist_company(self):
        response = self.client.get(reverse('employee_profile_by_person_company_api',
                                           kwargs={'person_id': self.normalize_key(3),
                                                    'company_id': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_profile_non_exist_user(self):
        response = self.client.get(reverse('employee_profile_by_company_user_api',
                                           kwargs={'user_id': self.normalize_key(sys.maxint),
                                                    'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_profile_exist_person_company_non_exist_profile(self):
        response = self.client.get(reverse('employee_profile_by_person_company_api',
                                           kwargs={'person_id': self.normalize_key(6),
                                                    'company_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_profile_exist_user_company_non_exist_profile(self):
        response = self.client.get(reverse('employee_profile_by_company_user_api',
                                           kwargs={'user_id': self.normalize_key(1),
                                                    'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_post_employee_profile_success(self):
        post_data = {
            "person": self.normalize_key(1),
            "company": self.normalize_key(1),
            "job_title": "Broker",
            "annual_base_salary": "40022.00",
            "start_date": "2008-03-01",
            "benefit_start_date": '2008-03-22',
            "end_date": "2008-06-01",
            "employment_type": "PartTime",
            "employment_status": "Terminated",
            "manager": 2,
            "employee_number": "ABC-999999"
        }
        response = self.client.post(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['person'], self.normalize_key(1))
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['job_title'], "Broker")
        self.assertEqual(result['annual_base_salary'], "40022.00")
        self.assertEqual(result['start_date'], "2008-03-01")
        self.assertEqual(result['benefit_start_date'], '2008-03-22')
        self.assertEqual(result['end_date'], "2008-06-01")
        self.assertEqual(result['employment_type'], "PartTime")
        self.assertEqual(result['employment_status'], "Terminated"),
        self.assertEqual(result['employee_number'], "ABC-999999"),
        self.assertIsNotNone(result['manager'])
        manager = result['manager']
        self.assertEqual(manager['id'], self.normalize_key(2))
        self.assertEqual(manager['first_name'], 'Christina')
        self.assertEqual(manager['last_name'], 'Cowell')

    def test_post_employee_profile_same_person_different_company_success(self):
        post_data = {
            "person": self.normalize_key(3),
            "company": self.normalize_key(2),
            "job_title": "Broker",
            "annual_base_salary": "40022.00",
            "start_date": "2008-03-01",
            "benefit_start_date": '2008-03-22',
            "end_date": "2008-06-01",
            "employment_type": "PartTime",
            "employment_status": "Terminated"
        }
        response = self.client.post(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company'], self.normalize_key(2))
        self.assertEqual(result['job_title'], "Broker")
        self.assertEqual(result['annual_base_salary'], "40022.00")
        self.assertEqual(result['start_date'], "2008-03-01")
        self.assertEqual(result['benefit_start_date'], '2008-03-22')
        self.assertEqual(result['end_date'], "2008-06-01")
        self.assertEqual(result['employment_type'], "PartTime")
        self.assertEqual(result['employment_status'], "Terminated")
        self.assertEqual(result['manager'], None)

    def test_post_employee_profile_non_exist_person_failure(self):
        post_data = {
            "person": self.normalize_key(sys.maxint),
            "company": self.normalize_key(1),
            "job_title": "Broker",
            "annual_base_salary": "40022.00",
            "start_date": "2008-03-01",
            "benefit_start_date": '2008-03-22',
            "end_date": "2008-06-01",
            "employment_type": "PartTime",
            "employment_status": "Terminated"
        }
        response = self.client.post(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_post_employee_profile_non_exist_company_failure(self):
        post_data = {
            "person": self.normalize_key(1),
            "company": self.normalize_key(sys.maxint),
            "job_title": "Broker",
            "annual_base_salary": "40022.00",
            "start_date": "2008-03-01",
            "benefit_start_date": '2008-03-22',
            "end_date": "2008-06-01",
            "employment_type": "PartTime",
            "employment_status": "Terminated"
        }
        response = self.client.post(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_post_employee_profile_duplicate_person_company_failure(self):
        post_data = {
            "person": self.normalize_key(3),
            "company": self.normalize_key(1),
            "job_title": "Broker",
            "annual_base_salary": "40022.00",
            "start_date": "2008-03-01",
            "benefit_start_date": '2008-03-22',
            "end_date": "2008-06-01",
            "employment_type": "PartTime",
            "employment_status": "Terminated"
        }
        response = self.client.post(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_post_employee_profile_duplicate_company_employee_number_failure(self):
        post_data = {
            "person": self.normalize_key(1),
            "company": self.normalize_key(1),
            "job_title": "Broker",
            "annual_base_salary": "40022.00",
            "start_date": "2008-03-01",
            "benefit_start_date": '2008-03-22',
            "end_date": "2008-06-01",
            "employment_type": "PartTime",
            "employment_status": "Terminated",
            "employee_number": "ABC-012345"
        }
        response = self.client.post(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_put_employee_profile_success(self):
        post_data = {
            "id": self.normalize_key(1),
            "person": self.normalize_key(3),
            "company": self.normalize_key(1),
            "pay_rate": self.normalize_key(1),
            "job_title": "Senior Broker",
            "annual_base_salary": "140022.00",
            "start_date": "2010-03-01",
            "benefit_start_date": '2010-03-22',
            "end_date": None,
            "employment_type": "FullTime",
            "employment_status": "Active",
            "manager": None,
            "employee_number": "ABC-999999"
        }
        response = self.client.put(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(1)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(1))
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertIn('pay_rate', result)
        self.assertIn('id', result['pay_rate'])
        self.assertEqual(result['pay_rate']['id'], self.normalize_key(1))
        self.assertEqual(result['job_title'], "Senior Broker")
        self.assertEqual(result['annual_base_salary'], "140022.00")
        self.assertEqual(result['start_date'], "2010-03-01")
        self.assertEqual(result['benefit_start_date'], "2010-03-22")
        self.assertEqual(result['end_date'], None)
        self.assertEqual(result['employment_type'], "FullTime")
        self.assertEqual(result['employment_status'], "Active")
        self.assertEqual(result['manager'], None)
        self.assertEqual(result['employee_number'], "ABC-999999")

    def test_put_employee_profile_with_ddj_success(self):
        post_data = {
            "id": self.normalize_key(1),
            "person": self.normalize_key(3),
            "company": self.normalize_key(1),
            "pay_rate": self.normalize_key(1),
            "job_title": "Senior Broker",
            "job": self.normalize_key(2),
            "department": self.normalize_key(1),
            "division": self.normalize_key(1),
            "annual_base_salary": "140022.00",
            "start_date": "2010-03-01",
            "benefit_start_date": '2010-03-22',
            "end_date": None,
            "employment_type": "FullTime",
            "employment_status": "Active",
            "manager": None,
            "employee_number": "ABC-999999"
        }
        response = self.client.put(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(1)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIn('id', result)
        self.assertEqual(result['id'], self.normalize_key(1))
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertIn('pay_rate', result)
        self.assertIn('id', result['pay_rate'])
        self.assertEqual(result['pay_rate']['id'], self.normalize_key(1))
        self.assertEqual(result['job_title'], "Senior Broker")
        self.assertEqual(result['job']['id'], self.normalize_key(2))
        self.assertEqual(result['department']['id'], self.normalize_key(1))
        self.assertEqual(result['division']['id'], self.normalize_key(1))
        self.assertEqual(result['annual_base_salary'], "140022.00")
        self.assertEqual(result['start_date'], "2010-03-01")
        self.assertEqual(result['benefit_start_date'], "2010-03-22")
        self.assertEqual(result['end_date'], None)
        self.assertEqual(result['employment_type'], "FullTime")
        self.assertEqual(result['employment_status'], "Active")
        self.assertEqual(result['manager'], None)
        self.assertEqual(result['employee_number'], "ABC-999999")

    def test_put_employee_profile_duplicate_company_employee_number_failure(self):
        post_data = {
            "id": self.normalize_key(1),
            "person": self.normalize_key(4),
            "company": self.normalize_key(1),
            "pay_rate": self.normalize_key(1),
            "job_title": "Senior Broker",
            "annual_base_salary": "140022.00",
            "start_date": "2010-03-01",
            "benefit_start_date": '2010-03-22',
            "end_date": None,
            "employment_type": "FullTime",
            "employment_status": "Active",
            "manager": None,
            "employee_number": "ABC-012345"
        }
        response = self.client.post(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}),
                                    data=json.dumps(post_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_delete_employee_profile_success(self):
        response = self.client.delete(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

    def test_delete_employee_profile_non_exist_failure(self):
        response = self.client.delete(reverse('employee_profile_api',
                                           kwargs={'pk': self.normalize_key(sys.maxint)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_get_employee_profile_by_company_pin_success(self):
        response = self.client.get(reverse('employee_profile_by_company_pin_api',
                                           kwargs={'company_id': self.normalize_key(1),
                                                   'pin': "1234"}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual("1234", result['pin'])
        self.assertEqual("https://www.google.com/", result['photo_url'])

    def test_get_employee_profile_by_company_pin_not_exist(self):
        response = self.client.get(reverse('employee_profile_by_company_pin_api',
                                           kwargs={'company_id': self.normalize_key(1),
                                                   'pin': "0000"}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_upload_new_photo_url(self):
        response = self.client.get(reverse('employee_profile_by_company_pin_api',
                                           kwargs={'company_id': self.normalize_key(1),
                                                   'pin': "1234"}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['person']['id'], self.normalize_key(4))
        self.assertIsNotNone(result['department'])
        self.assertEqual(result['department']['id'], self.normalize_key(1))
        employee_profile_id = result['id']
        new_photo_url = 'https://www.yahoo.com'
        result['person'] = self.normalize_key(4)
        result['photo_url'] = new_photo_url
        put_response = self.client.put(
            reverse('employee_profile_api',
                kwargs={'pk': employee_profile_id}),
            data=json.dumps(result),
            content_type='application/json'
        )
        self.assertEqual(put_response.status_code, 200)

        response_again = self.client.get(reverse('employee_profile_by_company_pin_api',
                                           kwargs={'company_id': self.normalize_key(1),
                                                   'pin': "1234"}))
        self.assertIsNotNone(response_again)
        self.assertEqual(response_again.status_code, 200)
        result_new = json.loads(response_again.content)
        self.assertEqual(result_new['pin'], "1234")
        self.assertEqual(result_new['photo_url'], new_photo_url)
