import json
import sys
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class DirectReportsViewTest(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person',
                '79_company_department', '82_company_job', '83_company_division',
                'employee_profile',
                '49_period_definition',
                '10_company',
                '23_auth_user',
                '34_company_user']

    def test_get_direct_reports_success(self):
        response = self.client.get(
            reverse('direct_reports_api',
                kwargs={
                    'comp_id': self.normalize_key(1),
                    'user_id': self.normalize_key(8)
                }
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['user_roles'][0]['id'], self.normalize_key(3))
        self.assertEqual(result['user_roles'][0]['company_user_type'], 'employee')
        self.assertEqual(result['user_roles'][0]['user']['first_name'], 'Simon')
        self.assertEqual(result['user_roles'][0]['user']['email'],
                         'user3@benefitmy.com')
        self.assertEqual(result['user_roles'][0]['new_employee'], True)

    def test_get_no_direct_reports_success(self):
        response = self.client.get(
            reverse('direct_reports_api',
                kwargs={
                    'comp_id': self.normalize_key(1),
                    'user_id': self.normalize_key(4)
                }
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['user_roles'], [])

    def test_get_bad_company_success(self):
        response = self.client.get(
            reverse('direct_reports_api',
                kwargs={
                    'comp_id': self.normalize_key(10),
                    'user_id': self.normalize_key(4)
                }
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['user_roles'], [])

class DirectReportCountViewTest(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person',
                '79_company_department', '82_company_job', '83_company_division',
                'employee_profile',
                '49_period_definition',
                '10_company',
                '23_auth_user',
                '34_company_user']

    def test_get_direct_report_count_success(self):
        response = self.client.get(
            reverse('direct_report_count_api',
                kwargs={
                    'comp_id': self.normalize_key(1),
                    'user_id': self.normalize_key(8)
                }
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['count'], 1)

    def test_get_no_direct_report_count_success(self):
        response = self.client.get(
            reverse('direct_report_count_api',
                kwargs={
                    'comp_id': self.normalize_key(1),
                    'user_id': self.normalize_key(4)
                }
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['count'], 0)

    def test_get_bad_company_success(self):
        response = self.client.get(
            reverse('direct_report_count_api',
                kwargs={
                    'comp_id': self.normalize_key(10),
                    'user_id': self.normalize_key(4)
                }
            )
        )
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['count'], 0)
