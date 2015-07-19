import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase

class CompanySupplementalLifeInsuranceTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['26_supplemental_life_insurance', '38_supplemental_life_rate',
    '39_company_supplement_life_insurance', '17_supplemental_life_insurance_condition',
    '10_company']

    def test_get_company_suppl_life(self):
        response = self.client.get(reverse('comp_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(result['supplemental_life_insurance_plan']['id'], self.normalize_key(1))


    def test_get_company_suppl_life_by_company(self):
        response = self.client.get(reverse('company_comp_suppl_life',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['company'], self.normalize_key(1))
        self.assertEqual(result[0]['supplemental_life_insurance_plan']['id'], self.normalize_key(1))

    def test_delete_company_suppl_life(self):
        response = self.client.get(reverse('comp_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('comp_suppl_life_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('comp_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_suppl_life(self):
        suppl_life_data = {"company": 2,
                           "supplemental_life_insurance_plan": 1}
        response = self.client.post(reverse('comp_suppl_life_api',
                                            kwargs={'pk': self.normalize_key(4)}),
                                            suppl_life_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('comp_suppl_life_api',
                                           kwargs={'pk': self.normalize_key(4)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(2))

        key = result['id']
        response = self.client.get(reverse('comp_suppl_life_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(2))
