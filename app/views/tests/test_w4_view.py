from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class w4TestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', '35_w4']

    def test_get_w4(self):
        response = self.client.get(reverse('w4_api',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['marriage'], 2)
        self.assertEqual(result['tax_credit'], 0)
        self.assertEqual(result['user'], 3)
        self.assertEqual(result['extra_amount'], '100.00')
        self.assertEqual(result['user_defined_points'], 5)
        self.assertEqual(result['calculated_points'], 3)



    def test_post_w4(self):

        w4_data = {
                "marriage": 5,
                "dependencies": 0,
                "head": 1,
                "tax_credit": 1,
                "calculated_points": 3,
                "user_defined_points": 5,
                "extra_amount": "100.00",
                "user": 1
                }

        response = self.client.post(reverse('w4_api', kwargs={'pk': self.normalize_key(1)}),
                                    w4_data)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('w4_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertEqual(result['marriage'], 5)
        self.assertEqual(result['tax_credit'], 1)
        self.assertEqual(result['user'], 1)
        self.assertEqual(result['extra_amount'], '100.00')
        self.assertEqual(result['user_defined_points'], 5)
        self.assertEqual(result['calculated_points'], 3)
