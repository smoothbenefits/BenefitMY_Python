import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class CompanyFsaTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['26_supplemental_life_insurance', '38_supplemental_life_rate', 
    '39_company_supplement_life_insurance', '17_supplemental_life_insurance_condition',
    '10_company', '44_person_company_suppl_life', '24_person', '23_auth_user']

    def test_get_person_company_suppl_life_by_person(self):
        response = self.client.get(reverse('person_person_supple_life',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['person'], self.normalize_key(3))
        self.assertEqual(result[0]['company_supplemental_life_insurance_plan']['id'], self.normalize_key(1))

    def test_get_person_company_suppl_life(self):
        response = self.client.get(reverse('person_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company_supplemental_life_insurance_plan']['id'], self.normalize_key(1))

    def test_delete_person_company_suppl_life(self):
        response = self.client.get(reverse('person_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('person_suppl_life_api', 
                                              kwargs={'pk': self.normalize_key(2)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('person_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(2)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_put_person_company_suppl_life(self):
        suppl_life_data = {
          "company_supplemental_life_insurance_plan": self.normalize_key(1),
          "person": self.normalize_key(3),
          "self_elected_amount": 10,
          "spouse_elected_amount": 10,
          "child_elected_amount": 10,
          "self_premium_per_month": 1.00,
          "spouse_premium_per_month": 1.00,
          "child_premium_per_month": 1.00,
          "self_condition": self.normalize_key(2),
          "spouse_condition": self.normalize_key(3)
        }
        response = self.client.put(reverse('person_suppl_life_api',
                                            kwargs={'pk': self.normalize_key(1)}),
                                            data=json.dumps(suppl_life_data),
                                            content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('person_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['self_elected_amount'], "10.00")
        self.assertEqual(result['spouse_elected_amount'], "10.00")
        self.assertEqual(result['child_elected_amount'], "10.00")
        self.assertEqual(result["self_premium_per_month"], "1.00")
        self.assertEqual(result["spouse_premium_per_month"], "1.00")
        self.assertEqual(result["child_premium_per_month"], "1.00")

    def test_post_person_company_suppl_life(self):
        suppl_life_data = {
          "company_supplemental_life_insurance_plan": 1,
          "person": 3,
          "self_elected_amount": 10,
          "spouse_elected_amount": 10,
          "child_elected_amount": 10,
          "self_premium_per_month": 1.00,
          "spouse_premium_per_month": 1.00,
          "child_premium_per_month": 1.00,
          "self_condition": 3,
          "spouse_condition": 3
        }
        response = self.client.post(reverse('person_suppl_life_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            suppl_life_data)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('person_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['person'], self.normalize_key(3))

        key = result['id']
        response = self.client.get(reverse('person_suppl_life_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['person'], self.normalize_key(3))
        self.assertEqual(result['company_supplemental_life_insurance_plan']['id'], self.normalize_key(1))
