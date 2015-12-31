import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class PersonCompanyHsaPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user', '61_company_group', '10_company', '24_person',
                '49_period_definition', '65_hsa_plan', 'sys_benefit_update_reason',
                'sys_benefit_update_reason_category']

    def test_get_person_company_hsa_insurance_success(self):
        response = self.client.get(reverse('person_hsa_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_hsa_plan']['id'], self.normalize_key(1))

    def test_get_person_hsa_invalid_person(self):
        response = self.client.get(reverse('person_hsa_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(100)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


    def test_post_person_company_hsa_success(self):
        std_data = {'person': self.normalize_key(4),
                    'company_hsa_plan': self.normalize_key(1),
                    'record_reason': self.normalize_key(1),
                    'amount_per_year': 500}
        response = self.client.post(reverse('person_hsa_plan_by_person_api',
                                            kwargs={'person_id': self.normalize_key(4)}),
                                            json.dumps(std_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('person_hsa_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(4)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_hsa_plan']['id'], self.normalize_key(1))
        self.assertEqual(result['record_reason']['id'], self.normalize_key(1))
        self.assertEqual(result['amount_per_year'], '500.00')

    def test_delete_person_hsa_plan_success(self):
        response = self.client.get(reverse('person_hsa_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIsNotNone(result)

        response = self.client.delete(reverse('person_hsa_plan_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('person_hsa_plan_by_person_api',
                                           kwargs={'person_id': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
