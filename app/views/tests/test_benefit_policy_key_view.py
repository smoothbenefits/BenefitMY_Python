import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class BenefitPolicyKeyTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['15_benefit_policy_key']
    def test_get_all_keys_success(self):
        response = self.client.get(reverse('benefit_policy_key_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)

        # Also assure that the ordering of the result is respecting 
        # the "rank" field properly
        for i in range(1, len(result)):
            self.assertTrue(result[i]['rank'] >= result[i-1]['rank'])    
