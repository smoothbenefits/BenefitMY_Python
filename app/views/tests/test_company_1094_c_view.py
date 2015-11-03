from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class Company1094CTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['10_company', '49_period_definition', '60_company_1094_c']

    def test_get_company_1094_c_success(self):
        response = self.client.get(reverse('company_1094_c_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)['member']
        self.assertEqual(type(result), dict)
        self.assertEqual(result['id'], self.normalize_key(1))
        self.assertEqual(result['member_of_aggregated_group'], True)
        self.assertEqual(result['company']['id'], self.normalize_key(1))
        self.assertEqual(result['number_of_1095c'], 50)
        self.assertEqual(result['authoritative_transmittal'], False)
        self.assertEqual(result['certifications_of_eligibility'], 'Qualifying Offer Method')
        self.assertEqual(result['created_at'], '2015-04-27T04:00:00Z')

        result = json.loads(response.content)['monthly_info']
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['minimum_essential_coverage'], True)
        self.assertEqual(result[0]['fulltime_employee_count'], 65)
        self.assertEqual(result[0]['total_employee_count'], 100)
        self.assertEqual(result[0]['aggregated_group'], True)
        self.assertEqual(result[0]['section_4980h_transition_relief'], '1A')
        self.assertEqual(result[0]['period'], 'All 12 Months')

    def test_get_company_1094_c_empty(self):
        response = self.client.get(reverse('company_1094_c_api',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(type(result['member']), dict)
        self.assertEqual(result['member']['company'], None)
        self.assertEqual(type(result['monthly_info']), list)
        self.assertEqual(len(result['monthly_info']), 0)

    def test_get_company_1094_c_not_exists(self):
        response = self.client.get(reverse('company_1094_c_api',
                                           kwargs={'pk': self.normalize_key(15)}))
        self.assertEqual(response.status_code, 404)

    def test_post_company_1094_c_success(self):
        new_1094_c = {
          'member': {
            'company': self.normalize_key(3),
            'number_of_1095c': 50,
            'authoritative_transmittal': False,
            'member_of_aggregated_group': True
          },
          'monthly_info': [{
            'company': self.normalize_key(3),
            'minimum_essential_coverage': True,
            'fulltime_employee_count': 65,
            'total_employee_count': 100,
            'aggregated_group': True,
            'section_4980h_transition_relief': '1A'
          }]
        }

        response = self.client.post(reverse('company_1094_c_api',
                                    kwargs={'pk': self.normalize_key(3)}),
                                    data=json.dumps(new_1094_c),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertTrue(type(result['member']), dict)
        self.assertTrue(type(result['monthly_info']), list)
        self.assertEqual(len(result['monthly_info']), 1)
        self.assertEqual(result['member']['id'], self.normalize_key(3))
        self.assertEqual(result['member']['number_of_1095c'], 50)
        self.assertEqual(result['member']['authoritative_transmittal'], False)
        self.assertEqual(result['member']['member_of_aggregated_group'], True)
        self.assertEqual(result['member']['certifications_of_eligibility'], 'Qualifying Offer Method')
