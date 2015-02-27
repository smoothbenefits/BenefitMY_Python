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

        self.assertEqual(result[1]['percentage'], '60.00')
        self.assertEqual(result[1]['user'], self.normalize_key(1))
        self.assertEqual(result[1]['bank_account']['attachment'], 's3://abcdfdsfddef')
        self.assertEqual(result[1]['bank_account']['routing'], '2121123456')
        self.assertEqual(result[1]['bank_account']['account'], '5432221211')

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

        response = self.client.delete(reverse('direct_deposit_api',
                                              kwargs={'pk': self.normalize_key(3)}))

        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result, [])

    """
    def test_post_direct_deposit(self):
        dd_data={ "bank_account": {
                                    "routing": "111121211234323256",
                                    "account": "543211221211",
                                    "account_type": "Saving",
                                    "bank_name": "Citi bank",
                                    "attachment": "s3://abcfdsfdfdsfdffddef",
                                    "user": 3
                                },
                    "amount": "10000.00",
                    "percentage": "0.00",
                    "user": 3
                }

        response = self.client.post(reverse('direct_deposit_api', kwargs={'pk': 1}),
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
        dd_data = {"routing1": "123422252226",
                   "account1": "54321222",
                   "account_type1": "Checking",
                   "bank_name1": "Bank of America",
                   "attachment1": "s3://abcdsddsdef",
                   "amount1": "0.00",
                   "percentage1": "40.00",
                   "routing2": "122211122",
                   "account2": "6789999990",
                   "account_type2": "Saving",
                   "bank_name2": "Citi Bank",
                   "attachment2": "s3://ab12222222cdefdfg",
                   "amount2": "0.00",
                   "percentage2": "60.00",
                   "user": 1}
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['routing1'], '123456')
        self.assertEqual(result['bank_name1'], 'Bank of America')
        self.assertEqual(result['bank_name1'], 'Bank of America')
        self.assertEqual(result['attachment1'], 's3://abcdef')
        self.assertEqual(result['account2'], '67890')

        response = self.client.put(reverse('direct_deposit_api', kwargs={'pk': 1}),
                                   dd_data,
                                   content_type='application/x-www-form-urlencoded')
        print response
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': 1}))
        print response
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['routing1'], '123422252226')
        self.assertEqual(result['bank_name1'], 'Bank of America')
        self.assertEqual(result['attachment1'], 's3://abcdsddsdef')
        self.assertEqual(result['account2'], '6789999990')
        """
