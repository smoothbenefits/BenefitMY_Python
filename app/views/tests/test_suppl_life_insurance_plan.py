import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class SupplementalLifeInsuranceTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['26_supplemental_life_insurance', '38_supplemental_life_rate', 
    '39_company_supplement_life_insurance', '17_supplemental_life_insurance_condition',
    '10_company']

    def test_get_suppl_life_insurance(self):
        response = self.client.get(reverse('suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['name'], "Health First")
        self.assertEqual(result['use_employee_age_for_spouse'], False)

        rates = result['supplemental_life_insurance_plan_rate']
        self.assertEqual(type(rates), list)
        self.assertEqual(len(rates), 27)

        rate = next(r for r in rates if r['id'] == self.normalize_key(6))
        self.assertEqual(rate['supplemental_life_insurance_plan'], self.normalize_key(1))
        self.assertEqual(rate['age_min'], 50)
        self.assertEqual(rate['age_max'], 55)
        self.assertEqual(rate['bind_type'], "self")
        self.assertEqual(rate['rate'], "0.08")
        self.assertEqual(rate['condition']['id'], self.normalize_key(2))

    def test_delete_suppl_life_insurance(self):
        response = self.client.get(reverse('suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('suppl_life_api', 
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_suppl_life(self):
        suppl_life_data = {"name": "Test SLI",
                           "use_employee_age_for_spouse": False,
                           "supplemental_life_insurance_plan_rate": [
                               {
                                   "supplemental_life_insurance_plan": 1,
                                   "age_min": 25,
                                   "age_max": 30,
                                   "bind_type": "self",
                                   "rate": 0.03,
                                   "condition": 2
                               }
                           ]}
        response = self.client.post(reverse('suppl_life_api',
                                            kwargs={'pk': self.normalize_key(4)}),
                                            data=json.dumps(suppl_life_data),
                                            content_type='application/json')
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('suppl_life_api',
                                           kwargs={'pk': self.normalize_key(4)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['name'], "Test SLI")

        key = result['id']
        response = self.client.get(reverse('suppl_life_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['name'], "Test SLI")


