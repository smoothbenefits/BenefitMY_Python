from django.test import TestCase
from django.core.urlresolvers import reverse
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
