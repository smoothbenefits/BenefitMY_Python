from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class Company1095CTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['10_company', '49_period_definition', '52_company_1095_c']

    def test_get_company_1095_c_success(self):
        response = self.client.get(reverse('company_1095_c_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['id'], self.normalize_key(1))
        self.assertEqual(result[0]['offer_of_coverage'], '1A')
        self.assertEqual(result[0]['company']['id'], self.normalize_key(1))
        self.assertEqual(result[0]['employee_share'], '34.00')
        self.assertEqual(result[0]['safe_harbor'], None)
        self.assertEqual(result[0]['period'], 'All 12 Months')
        self.assertEqual(result[0]['created_at'], '2015-04-27T04:00:00Z')

    def test_get_company_1095_c_empty(self):
        response = self.client.get(reverse('company_1095_c_api',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) == 0)

    def test_get_company_1095_c_not_exists(self):
        response = self.client.get(reverse('company_1095_c_api',
                                           kwargs={'pk': self.normalize_key(15)}))
        self.assertEqual(response.status_code, 404)

    def test_post_company_1095_c_success(self):
        new_1095_c = [{'company': self.normalize_key(3), 
                       'offer_of_coverage': '1I',
                       'employee_share': '44.00',
                       'safe_harbor': None,
                       'period': 'All 12 Months'}]

        response = self.client.post(reverse('company_1095_c_api',
                                    kwargs={'pk': self.normalize_key(3)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['id'], self.normalize_key(6))
        self.assertEqual(result[0]['offer_of_coverage'], '1I')
        self.assertEqual(result[0]['company'], 3)
        self.assertEqual(result[0]['employee_share'], '44.00')
        self.assertEqual(result[0]['safe_harbor'], None)
        self.assertEqual(result[0]['period'], 'All 12 Months')

    def test_post_company_1095_c_multiple_success(self):
        new_1095_c = [{'company': self.normalize_key(4), 
                       'offer_of_coverage': '1C',
                       'employee_share': '66.00',
                       'safe_harbor': None,
                       'period': 'Sept'},
                       {'company': self.normalize_key(4), 
                       'offer_of_coverage': '1C',
                       'employee_share': '66.00',
                       'safe_harbor': None,
                       'period': 'Oct'},
                       {'company': self.normalize_key(4), 
                       'offer_of_coverage': '1C',
                       'employee_share': '66.00',
                       'safe_harbor': None,
                       'period': 'Nov'},
                       {'company': self.normalize_key(4), 
                       'offer_of_coverage': '1C',
                       'employee_share': '66.00',
                       'safe_harbor': None,
                       'period': 'Dec'}]

        response = self.client.post(reverse('company_1095_c_api',
                                    kwargs={'pk': self.normalize_key(4)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) == 4)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['offer_of_coverage'], '1C')
        self.assertEqual(result[0]['company'], 4)
        self.assertEqual(result[0]['employee_share'], '66.00')
        self.assertEqual(result[0]['safe_harbor'], None)
        self.assertEqual(result[0]['period'], 'Sept')
        self.assertEqual(type(result[1]), dict)
        self.assertEqual(result[1]['offer_of_coverage'], '1C')
        self.assertEqual(result[1]['company'], 4)
        self.assertEqual(result[1]['employee_share'], '66.00')
        self.assertEqual(result[1]['safe_harbor'], None)
        self.assertEqual(result[1]['period'], 'Oct')
        self.assertEqual(type(result[2]), dict)
        self.assertEqual(result[2]['offer_of_coverage'], '1C')
        self.assertEqual(result[2]['company'], 4)
        self.assertEqual(result[2]['employee_share'], '66.00')
        self.assertEqual(result[2]['safe_harbor'], None)
        self.assertEqual(result[2]['period'], 'Nov')
        self.assertEqual(type(result[3]), dict)
        self.assertEqual(result[3]['offer_of_coverage'], '1C')
        self.assertEqual(result[3]['company'], 4)
        self.assertEqual(result[3]['employee_share'], '66.00')
        self.assertEqual(result[3]['safe_harbor'], None)
        self.assertEqual(result[3]['period'], 'Dec')

    def test_post_company_1095_c_update_success(self):

        new_1095_c = [{'company': self.normalize_key(3), 
                       'offer_of_coverage': '1D',
                       'employee_share': '22.00',
                       'safe_harbor': None,
                       'period': 'All 12 Months'}]

        response = self.client.post(reverse('company_1095_c_api',
                                    kwargs={'pk': self.normalize_key(3)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['offer_of_coverage'], '1D')
        self.assertEqual(result[0]['company'], 3)
        self.assertEqual(result[0]['employee_share'], '22.00')
        self.assertEqual(result[0]['safe_harbor'], None)
        self.assertEqual(result[0]['period'], 'All 12 Months')

        new_1095_c = [{'company': self.normalize_key(3), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Sept'},
                       {'company': self.normalize_key(3), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Oct'},
                       {'company': self.normalize_key(3), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Nov'},
                       {'company': self.normalize_key(3), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Dec'}]

        response = self.client.post(reverse('company_1095_c_api',
                                    kwargs={'pk': self.normalize_key(3)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) == 4)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['offer_of_coverage'], '1C')
        self.assertEqual(result[0]['company'], 3)
        self.assertEqual(result[0]['employee_share'], '55.00')
        self.assertEqual(result[0]['safe_harbor'], None)
        self.assertEqual(result[0]['period'], 'Sept')
        self.assertEqual(type(result[1]), dict)
        self.assertEqual(result[1]['offer_of_coverage'], '1C')
        self.assertEqual(result[1]['company'], 3)
        self.assertEqual(result[1]['employee_share'], '55.00')
        self.assertEqual(result[1]['safe_harbor'], None)
        self.assertEqual(result[1]['period'], 'Oct')
        self.assertEqual(type(result[2]), dict)
        self.assertEqual(result[2]['offer_of_coverage'], '1C')
        self.assertEqual(result[2]['company'], 3)
        self.assertEqual(result[2]['employee_share'], '55.00')
        self.assertEqual(result[2]['safe_harbor'], None)
        self.assertEqual(result[2]['period'], 'Nov')
        self.assertEqual(type(result[3]), dict)
        self.assertEqual(result[3]['offer_of_coverage'], '1C')
        self.assertEqual(result[3]['company'], 3)
        self.assertEqual(result[3]['employee_share'], '55.00')
        self.assertEqual(result[3]['safe_harbor'], None)
        self.assertEqual(result[3]['period'], 'Dec')

    def test_post_company_1095_c_no_company(self):
        new_1095_c = [{'company': self.normalize_key(13), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Sept'},
                       {'company': self.normalize_key(13), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Oct'},
                       {'company': self.normalize_key(13), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Nov'},
                       {'company': self.normalize_key(13), 
                       'offer_of_coverage': '1C',
                       'employee_share': '55.00',
                       'safe_harbor': None,
                       'period': 'Dec'}]

        response = self.client.post(reverse('company_1095_c_api',
                                    kwargs={'pk': self.normalize_key(13)}),
                                    data=json.dumps(new_1095_c),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)


