import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class EmployeeForm1095CTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user', '13_benefit_type',
                '34_company_user', 'employee_profile', '60_company_1094_c', '55_employee_1095_c']

    def test_get_employee_1094_c_success(self):
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('employee_1094_c_form_api',
                                               kwargs={'pk': self.normalize_key(3)}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("login failed!")


    def test_get_company_form_1094_c_non_exist(self):
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('employee_1094_c_form_api',
                                               kwargs={'pk': self.normalize_key(10)}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 404)
        else:
            self.assertFalse("login failed!")
