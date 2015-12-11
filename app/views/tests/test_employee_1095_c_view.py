from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class Company1095CTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['10_company', '49_period_definition', '55_employee_1095_c',
                '24_person', '23_auth_user']

    def test_get_company_1095_c_success(self):
        response = self.client.get(reverse('employee_1095_c_api',
                                           kwargs={'person_id': self.normalize_key(3),
                                                   'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['id'], self.normalize_key(1))
        self.assertEqual(result[0]['company']['id'], self.normalize_key(1))
        self.assertEqual(result[0]['offer_of_coverage'], '1B')
        self.assertEqual(result[0]['employee_share'], '23.00')
        self.assertEqual(result[0]['safe_harbor'], 'SAFE')
        self.assertEqual(result[0]['period'], 'All 12 Months')
        self.assertEqual(result[0]['created_at'], '2015-04-27T04:00:00Z')

    def test_get_employee_1095_c_empty(self):
        response = self.client.get(reverse('employee_1095_c_api',
                                           kwargs={'person_id': self.normalize_key(1),
                                                   'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) == 0)

    def test_post_employee_1095_c_success(self):
        new_1095_c = [{'company': self.normalize_key(1),
                       'person': self.normalize_key(4),
                       'offer_of_coverage': '1E',
                       'employee_share': 54.01,
                       'safe_harbor': '12 MONTH',
                       'period': 'All 12 Months'}]

        response = self.client.post(reverse('employee_1095_c_api',
                                    kwargs={'person_id': self.normalize_key(4),
                                            'company_id': self.normalize_key(1)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        savedResponse = json.loads(response.content)
        result = savedResponse['saved']
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['id'], self.normalize_key(6))
        self.assertEqual(result[0]['company'], 1)
        self.assertEqual(result[0]['person'], 4)
        self.assertEqual(result[0]['offer_of_coverage'], '1E')
        self.assertEqual(result[0]['employee_share'], '54.01')
        self.assertEqual(result[0]['safe_harbor'], '12 MONTH')
        self.assertEqual(result[0]['period'], 'All 12 Months')

    def test_post_employee_1095_c_multiple_success(self):
        new_1095_c = [{'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'Jan'},
                       {'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'Feb'},
                       {'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'Mar'},
                       {'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'May'}]

        response = self.client.post(reverse('employee_1095_c_api',
                                    kwargs={'person_id': self.normalize_key(4),
                                            'company_id': self.normalize_key(1)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        savedResponse = json.loads(response.content)
        result = savedResponse['saved']
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) == 4)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['person'], 4)
        self.assertEqual(result[0]['offer_of_coverage'], '1F')
        self.assertEqual(result[0]['employee_share'], '1.23')
        self.assertEqual(result[0]['safe_harbor'], None)
        self.assertEqual(result[0]['period'], 'Jan')
        self.assertEqual(type(result[1]), dict)
        self.assertEqual(result[1]['person'], 4)
        self.assertEqual(result[1]['offer_of_coverage'], '1F')
        self.assertEqual(result[1]['employee_share'], '1.23')
        self.assertEqual(result[1]['safe_harbor'], None)
        self.assertEqual(result[1]['period'], 'Feb')
        self.assertEqual(type(result[2]), dict)
        self.assertEqual(result[2]['person'], 4)
        self.assertEqual(result[2]['offer_of_coverage'], '1F')
        self.assertEqual(result[2]['employee_share'], '1.23')
        self.assertEqual(result[2]['safe_harbor'], None)
        self.assertEqual(result[2]['period'], 'Mar')
        self.assertEqual(type(result[3]), dict)
        self.assertEqual(result[3]['person'], 4)
        self.assertEqual(result[3]['offer_of_coverage'], '1F')
        self.assertEqual(result[3]['employee_share'], '1.23')
        self.assertEqual(result[3]['safe_harbor'], None)
        self.assertEqual(result[3]['period'], 'May')

    def test_post_company_1095_c_update_success(self):

        new_1095_c = [{'person': self.normalize_key(3),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1E',
                       'employee_share': 54.01,
                       'safe_harbor': None,
                       'period': 'All 12 Months'}]

        response = self.client.post(reverse('employee_1095_c_api',
                                    kwargs={'person_id': self.normalize_key(3),
                                            'company_id': self.normalize_key(1)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        savedResponse = json.loads(response.content)
        result = savedResponse['saved']
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['person'], 3)
        self.assertEqual(result[0]['company'], 1)
        self.assertEqual(result[0]['offer_of_coverage'], '1E')
        self.assertEqual(result[0]['employee_share'], '54.01')
        self.assertEqual(result[0]['safe_harbor'], None)
        self.assertEqual(result[0]['period'], 'All 12 Months')

        new_1095_c = [{'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': 'SAFE',
                       'period': 'Sept'},
                       {'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': 'SAFE',
                       'period': 'Oct'},
                       {'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': 'SAFE',
                       'period': 'Nov'},
                       {'person': self.normalize_key(4),
                       'company': self.normalize_key(1),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': 'SAFE',
                       'period': 'Dec'}]

        response = self.client.post(reverse('employee_1095_c_api',
                                    kwargs={'person_id': self.normalize_key(4),
                                            'company_id': self.normalize_key(1)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        savedResponse = json.loads(response.content)
        result = savedResponse['saved']
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) == 4)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['person'], 4)
        self.assertEqual(result[0]['company'], 1)
        self.assertEqual(result[0]['offer_of_coverage'], '1F')
        self.assertEqual(result[0]['employee_share'], '1.23')
        self.assertEqual(result[0]['safe_harbor'], 'SAFE')
        self.assertEqual(result[0]['period'], 'Sept')
        self.assertEqual(type(result[1]), dict)
        self.assertEqual(result[1]['person'], 4)
        self.assertEqual(result[1]['company'], 1)
        self.assertEqual(result[1]['offer_of_coverage'], '1F')
        self.assertEqual(result[1]['employee_share'], '1.23')
        self.assertEqual(result[1]['safe_harbor'], 'SAFE')
        self.assertEqual(result[1]['period'], 'Oct')
        self.assertEqual(type(result[2]), dict)
        self.assertEqual(result[2]['person'], 4)
        self.assertEqual(result[2]['company'], 1)
        self.assertEqual(result[2]['offer_of_coverage'], '1F')
        self.assertEqual(result[2]['employee_share'], '1.23')
        self.assertEqual(result[2]['safe_harbor'], 'SAFE')
        self.assertEqual(result[2]['period'], 'Nov')
        self.assertEqual(type(result[3]), dict)
        self.assertEqual(result[3]['person'], 4)
        self.assertEqual(result[3]['company'], 1)
        self.assertEqual(result[3]['offer_of_coverage'], '1F')
        self.assertEqual(result[3]['employee_share'], '1.23')
        self.assertEqual(result[3]['safe_harbor'], 'SAFE')
        self.assertEqual(result[3]['period'], 'Dec')

    def test_post_company_1095_c_no_company(self):
        new_1095_c = [{'company': self.normalize_key(13),
                       'person': self.normalize_key(50),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'Sept'},
                       {'company': self.normalize_key(13),
                       'person': self.normalize_key(50),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'Oct'},
                       {'company': self.normalize_key(13),
                       'person': self.normalize_key(50),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'Nov'},
                       {'company': self.normalize_key(13),
                       'person': self.normalize_key(50),
                       'offer_of_coverage': '1F',
                       'employee_share': 1.23,
                       'safe_harbor': None,
                       'period': 'Dec'}]

        response = self.client.post(reverse('employee_1095_c_api',
                                    kwargs={'person_id': self.normalize_key(50),
                                            'company_id': self.normalize_key(13)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
