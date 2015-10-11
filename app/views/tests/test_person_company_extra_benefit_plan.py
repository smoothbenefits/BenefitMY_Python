import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class PersonCompanyExtraBenefitPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['56_company_extra_benefit_plan', '58_person_company_extra_benefit_plan',
                '57_extra_benefit_item', '59_person_company_extra_benefit_plan_item',
                '49_period_definition', '10_company', '24_person', '23_auth_user',
                'sys_benefit_update_reason', 'sys_benefit_update_reason_category']

    def test_get_person_company_extra_benefit_plan_by_person(self):
        response = self.client.get(reverse('person_company_extra_benefit_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['person'], self.normalize_key(3))
        self.assertEqual(result[0]['company_plan']['id'], self.normalize_key(1))
        self.assertEqual(len(result[0]['plan_items']), 1)
        self.assertEqual(result[0]['plan_items'][0]['id'], self.normalize_key(1))
        self.assertEqual(result[0]['plan_items'][0]['extra_benefit_item']['id'], self.normalize_key(2))

    def test_get_person_company_extra_benefit_plan(self):
        response = self.client.get(reverse('person_company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company_plan']['id'], self.normalize_key(1))
        self.assertEqual(len(result['plan_items']), 1)
        self.assertEqual(result['plan_items'][0]['id'], self.normalize_key(1))
        self.assertEqual(result['plan_items'][0]['extra_benefit_item']['id'], self.normalize_key(2))

    def test_delete_person_company_extra_benefit_plan(self):
        response = self.client.get(reverse('person_company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('person_company_extra_benefit_plan_api',
                                              kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('person_company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_put_person_company_extra_benefit_plan(self):
        put_data = {
          "company_plan": self.normalize_key(1),
          "person": self.normalize_key(3),
          "plan_items": [
            {
                "id": self.normalize_key(1),
                "person_company_extra_benefit_plan": self.normalize_key(1),
                "extra_benefit_item": self.normalize_key(2)
            },
            {
                "person_company_extra_benefit_plan": self.normalize_key(1),
                "extra_benefit_item": self.normalize_key(1)
            }
          ]}
        response = self.client.put(reverse('person_company_extra_benefit_plan_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                            data=json.dumps(put_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('person_company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(len(result['plan_items']), 2)

    def test_post_person_company_extra_benefit_plan(self):
        post_data = {
          "company_plan": self.normalize_key(1),
          "person": self.normalize_key(4),
          "plan_items": [
            {
                "extra_benefit_item": self.normalize_key(2)
            },
            {
                "extra_benefit_item": self.normalize_key(1)
            }
          ]}

        response = self.client.post(reverse('person_company_extra_benefit_plan_api',
                                            kwargs={'pk': self.normalize_key(4)}),
                                            data=json.dumps(post_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('person_company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(4))

        key = result['id']
        response = self.client.get(reverse('person_company_extra_benefit_plan_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['person'], self.normalize_key(4))
        self.assertEqual(len(result['plan_items']), 2)
