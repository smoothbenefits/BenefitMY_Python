from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class CompanyFsaTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['37_fsa_plan', '23_auth_user', '24_person', '10_company',
                '49_period_definition', '42_company_fsa', '43_fsa', 'sys_benefit_update_reason',
                'sys_benefit_update_reason_category']

    def test_get_user_company_fsa_by_user(self):
        response = self.client.get(reverse('user_company_fsa_api',
                                           kwargs={'user_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(1))
        self.assertEqual(result['company_fsa_plan'], self.normalize_key(1))

    def test_get_user_company_fsa(self):
        response = self.client.get(reverse('company_users_fsa_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['user'], self.normalize_key(2))
        self.assertEqual(result['company_fsa_plan'], self.normalize_key(1))

    def test_delete_user_company_fsa(self):
        response = self.client.get(reverse('company_users_fsa_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('company_users_fsa_api',
                                              kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_users_fsa_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_put_user_company_fsa(self):
        fsa_data = {
          "id": self.normalize_key(1),
          "user": self.normalize_key(1),
          "primary_amount_per_year": "500.00",
          "dependent_amount_per_year": "500.00",
          "update_reason": "new update",
          "company_fsa_plan": self.normalize_key(1),
          "record_reason": self.normalize_key(1),
          "record_reason_note": "Test Note"
        }
        response = self.client.put(reverse('company_users_fsa_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                            data=json.dumps(fsa_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('company_users_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['primary_amount_per_year'], "500.00")
        self.assertEqual(result['dependent_amount_per_year'], "500.00")
        self.assertEqual(result['record_reason']['id'], self.normalize_key(1))
        self.assertEqual(result['record_reason_note'], 'Test Note')
