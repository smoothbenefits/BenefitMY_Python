from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import MULTIPART_CONTENT
from view_test_base import ViewTestBase
import json


class DirectDepositTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['direct_deposit', 'user_bank_account', '23_auth_user']

    def test_get_direct_deposit(self):
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)

        self.assertEqual(result[0]['percentage'], '40.00')
        self.assertEqual(result[0]['user'], self.normalize_key(1))
        self.assertEqual(result[0]['bank_account']['attachment'], 's3://abcdef')
        self.assertEqual(result[0]['bank_account']['routing'], '123456')
        self.assertEqual(result[0]['bank_account']['account'], '54321')
        self.assertEqual(result[0]['remainder_of_all'], False)

        self.assertEqual(result[1]['percentage'], '60.00')
        self.assertEqual(result[1]['user'], self.normalize_key(1))
        self.assertEqual(result[1]['bank_account']['attachment'], 's3://abcdfdsfddef')
        self.assertEqual(result[1]['bank_account']['routing'], '2121123456')
        self.assertEqual(result[1]['bank_account']['account'], '5432221211')
        self.assertEqual(result[1]['remainder_of_all'], False)

    def test_delete_direct_deposit(self):
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0]['amount'], '8210.00')
        self.assertEqual(result[0]['user'], self.normalize_key(2))
        self.assertEqual(result[0]['id'], self.normalize_key(3))
        self.assertEqual(result[0]['bank_account']['attachment'], 's3://abcfdsfdfdsfddef')
        self.assertEqual(result[0]['bank_account']['routing'], '11112121123456')
        self.assertEqual(result[0]['bank_account']['account'], '543211221211')
        self.assertEqual(result[0]['remainder_of_all'], False)

        self.assertEqual(result[1]['amount'], '0.00')
        self.assertEqual(result[1]['user'], self.normalize_key(2))
        self.assertEqual(result[1]['id'], self.normalize_key(4))
        self.assertEqual(result[1]['bank_account']['attachment'], 's3://54654654fdsafdsaf')
        self.assertEqual(result[1]['bank_account']['routing'], '4324234')
        self.assertEqual(result[1]['bank_account']['account'], '5653547665653')
        self.assertEqual(result[1]['remainder_of_all'], True)

        response = self.client.delete(reverse('direct_deposit_api',
                                              kwargs={'pk': self.normalize_key(3)}))

        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result[0]['amount'], '0.00')
        self.assertEqual(result[0]['user'], self.normalize_key(2))
        self.assertEqual(result[0]['id'], self.normalize_key(4))
        self.assertEqual(result[0]['bank_account']['attachment'], 's3://54654654fdsafdsaf')
        self.assertEqual(result[0]['bank_account']['routing'], '4324234')
        self.assertEqual(result[0]['bank_account']['account'], '5653547665653')
        self.assertEqual(result[0]['remainder_of_all'], True)


    """ post and put with nested data structure does not work, work in progress
    def test_post_direct_deposit(self):
        dd_data = [{"user": 1,
                   "bank_account": {
                       "routing": "2121",
                       "account": "54321",
                       "account_type": "Saving",
                       "bank_name": "Bank of America",
                       "attachment": "s3://a",
                       "user": 1},
                    "amount": "0.00",
                    "percentage": "70.00"},
                   {"user": 1,
                    "bank_account": {
                       "routing": "111",
                       "account": "2222",
                       "account_type": "Saving",
                       "bank_name": "Bank of America",
                       "attachment": "s3://a",
                       "user": 1},
                    "amount": "0.00",
                    "percentage": "30.00"}
                   ]


        response = self.client.post(reverse('direct_deposit_api', kwargs={'pk': self.normalize_key(1)}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)

        self.assertEqual(result[0]['amount'], '10000.00')
        self.assertEqual(result[0]['user'], 3)
        self.assertEqual(result[0]['bank_account']['attachment'], 's3://abcfdsfdfdsfddef')
        self.assertEqual(result[0]['bank_account']['routing'], '111121211234323256')
        self.assertEqual(result[0]['bank_account']['account'], '543211221211')

    def test_put_direct_deposit(self):
        dd_data = {"user": 1,
                   "bank_account": {
                       "routing": "2121",
                       "account": "54321",
                       "account_type": "Saving",
                       "bank_name": "Bank of America",
                       "attachment": "s3://a",
                       "user": 1},
                "amount": "0.00",
                "percentage": "70.00"}


        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)

        self.assertEqual(result[0]['percentage'], '40.00')
        self.assertEqual(result[0]['user'], self.normalize_key(1))
        self.assertEqual(result[0]['bank_account']['attachment'], 's3://abcdef')
        self.assertEqual(result[0]['bank_account']['routing'], '123456')
        self.assertEqual(result[0]['bank_account']['account'], '54321')

        response = self.client.put(reverse('direct_deposit_api', kwargs={'pk': self.normalize_key(1)}),
                                   dd_data,
                                   content_type='application/x-www-form-urlencoded')
        print response
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        print response
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result[0]['percentage'], '70.00')
        self.assertEqual(result[0]['user'], self.normalize_key(1))
        self.assertEqual(result[0]['bank_account']['attachment'], 's3://a')
        self.assertEqual(result[0]['bank_account']['routing'], '2121')
        self.assertEqual(result[0]['bank_account']['account'], '54321')
        """
