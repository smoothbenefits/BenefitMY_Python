import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class PersonCompanyHraPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['46_hra_plan', '47_company_hra_plan', '48_person_company_hra_plan',
                '49_period_definition', '10_company', '24_person', '23_auth_user', 
                'sys_benefit_update_reason', 'sys_benefit_update_reason_category']

    def test_get_person_company_hra_plan_by_person(self):
        response = self.client.get(reverse('person_company_hra_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['person'], self.normalize_key(3))
        self.assertEqual(result[0]['company_hra_plan']['id'], self.normalize_key(1))

    def test_get_person_company_hra_plan(self):
        response = self.client.get(reverse('person_company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company_hra_plan']['id'], self.normalize_key(1))

    def test_delete_person_company_hra_plan(self):
        response = self.client.get(reverse('person_company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('person_company_hra_plan_api',
                                              kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('person_company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_put_person_company_hra_plan(self):
        put_data = {
          "company_hra_plan": self.normalize_key(2),
          "person": self.normalize_key(3),
          "record_reason": self.normalize_key(1),
          "record_reason_note": "Test Note"}
        response = self.client.put(reverse('person_company_hra_plan_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                            data=json.dumps(put_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('person_company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_hra_plan']['id'], self.normalize_key(2))
        self.assertEqual(result['record_reason']['id'], self.normalize_key(1))
        self.assertEqual(result['record_reason_note'], 'Test Note')

    def test_post_person_company_hra_plan(self):
        post_data = {
          "company_hra_plan": 2,
          "person": 3,
          "record_reason": self.normalize_key(1)
        }

        response = self.client.post(reverse('person_company_hra_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            data=json.dumps(post_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('person_company_hra_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(3))

        key = result['id']
        response = self.client.get(reverse('person_company_hra_plan_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company_hra_plan']['id'], self.normalize_key(2))
        self.assertEqual(result['record_reason']['id'], self.normalize_key(1))
        self.assertIsNone(result['record_reason_note'])
