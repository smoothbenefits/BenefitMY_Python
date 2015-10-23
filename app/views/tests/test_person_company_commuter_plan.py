import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class PersonCompanyCommuterPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['53_company_commuter_plan', '54_person_company_commuter_plan',
                '49_period_definition', '10_company', '24_person', '23_auth_user']

    def test_get_person_company_commuter_plan_by_person(self):
        response = self.client.get(reverse('person_company_commuter_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['person'], self.normalize_key(3))
        self.assertEqual(result[0]['company_commuter_plan']['id'], self.normalize_key(1))
        self.assertEqual(float(result[0]['monthly_amount_transit_pre_tax']), 10.50)
        self.assertEqual(float(result[0]['monthly_amount_transit_post_tax']), 30.22)
        self.assertEqual(float(result[0]['monthly_amount_parking_pre_tax']), 50)
        self.assertEqual(float(result[0]['monthly_amount_parking_post_tax']), 10.11)

    def test_get_person_company_commuter_plan(self):
        response = self.client.get(reverse('person_company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company_commuter_plan']['id'], self.normalize_key(1))
        self.assertEqual(float(result['monthly_amount_transit_pre_tax']), 10.50)
        self.assertEqual(float(result['monthly_amount_transit_post_tax']), 30.22)
        self.assertEqual(float(result['monthly_amount_parking_pre_tax']), 50)
        self.assertEqual(float(result['monthly_amount_parking_post_tax']), 10.11)

    def test_delete_person_company_commuter_plan(self):
        response = self.client.get(reverse('person_company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('person_company_commuter_plan_api',
                                              kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('person_company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_put_person_company_commuter_plan(self):
        put_data = {
          "monthly_amount_transit_pre_tax": 1,
          "monthly_amount_transit_post_tax": 2,
          "monthly_amount_parking_pre_tax": 3,
          "monthly_amount_parking_post_tax": 4,
          "company_commuter_plan": self.normalize_key(2),
          "person": self.normalize_key(3)}
        response = self.client.put(reverse('person_company_commuter_plan_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                            data=json.dumps(put_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('person_company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_commuter_plan']['id'], self.normalize_key(2))
        self.assertEqual(float(result['monthly_amount_transit_pre_tax']), 1)
        self.assertEqual(float(result['monthly_amount_transit_post_tax']), 2)
        self.assertEqual(float(result['monthly_amount_parking_pre_tax']), 3)
        self.assertEqual(float(result['monthly_amount_parking_post_tax']), 4)

    def test_post_person_company_commuter_plan(self):
        post_data = {
          "company_commuter_plan": 2,
          "person": 3,
          "monthly_amount_transit_pre_tax": 1,
          "monthly_amount_transit_post_tax": 2,
          "monthly_amount_parking_pre_tax": 3,
          "monthly_amount_parking_post_tax": 4,
        }

        response = self.client.post(reverse('person_company_commuter_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            data=json.dumps(post_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('person_company_commuter_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(3))

        key = result['id']
        response = self.client.get(reverse('person_company_commuter_plan_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company_commuter_plan']['id'], self.normalize_key(2))
        self.assertEqual(float(result['monthly_amount_transit_pre_tax']), 1)
        self.assertEqual(float(result['monthly_amount_transit_post_tax']), 2)
        self.assertEqual(float(result['monthly_amount_parking_pre_tax']), 3)
        self.assertEqual(float(result['monthly_amount_parking_post_tax']), 4)
