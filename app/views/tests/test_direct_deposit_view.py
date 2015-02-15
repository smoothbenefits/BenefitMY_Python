from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import MULTIPART_CONTENT
import json


class DirectDepositTestCase(TestCase):
    # your fixture files here
    fixtures = ['direct_deposit', '23_auth_user']

    def test_get_direct_deposit(self):
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

        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': 2}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['percentage2'], '60.00')
        self.assertEqual(result['bank_name2'], 'Citi Bank')
        self.assertEqual(result['bank_name1'], 'Bank of America')
        self.assertEqual(result['account2'], '6789999990')

    def test_delete_direct_deposit(self):
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

        response = self.client.delete(reverse('direct_deposit_api',
                                              kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_direct_deposit(self):
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
                   "user": 3}
        response = self.client.post(reverse('direct_deposit_api', kwargs={'pk': 1}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('direct_deposit_api',
                                           kwargs={'pk': 3}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['routing1'], '123422252226')
        self.assertEqual(result['bank_name1'], 'Bank of America')
        self.assertEqual(result['attachment1'], 's3://abcdsddsdef')
        self.assertEqual(result['account2'], '6789999990')

        #Test post duplicate data
        response = self.client.post(reverse('direct_deposit_api', kwargs={'pk': 1}),
                                    dd_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 409)

    """
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
