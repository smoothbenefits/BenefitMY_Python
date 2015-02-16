from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json

'''
class WaivedBenefitTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['31_company_benefit_plan_option', '21_benefit_plan', '10_company', '13_benefit_type',
                'waived_benefit', '23_auth_user']

    def test_user_waived_benefit(self):
        response = self.client.get(reverse('user_waived_benefit_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0]['company']['name'], 'Startup.Com')
        self.assertEqual(result[0]['benefit_type']['name'], 'Vision')
        self.assertEqual(result[0]['user']['first_name'], 'John')


    def test_company_waived_benefit(self):
        response = self.client.get(reverse('company_waived_benefit_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0]['company']['name'], 'Startup.Com')
        self.assertEqual(result[0]['benefit_type']['name'], 'Vision')
        self.assertEqual(result[0]['user']['first_name'], 'John')
'''