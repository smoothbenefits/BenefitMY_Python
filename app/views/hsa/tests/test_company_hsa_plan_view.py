import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class CompanyHsaPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['65_hsa_plan', '23_auth_user', '61_company_group', '24_person',
                '49_period_definition', '10_company', 'sys_benefit_update_reason',
                'sys_benefit_update_reason_category']

    def test_get_company_hsa_insurance_success(self):
        response = self.client.get(reverse('company_hsa_plan_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 1)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(len(result['company_groups']), 2)


    def test_get_company_hsa_invalid_company(self):
        response = self.client.get(reverse('company_hsa_plan_company_api',
                                           kwargs={'company_id': self.normalize_key(100)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(len(array), 0)


    def test_post_company_hsa_success(self):
        std_data = {'company': self.normalize_key(3),
                    'name': "TESTING"}
        response = self.client.post(reverse('company_hsa_plan_company_api',
                                            kwargs={'company_id': self.normalize_key(3)}),
                                            json.dumps(std_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_hsa_plan_company_api',
                                           kwargs={'company_id': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 1)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(3))
        self.assertEqual(len(result['company_groups']), 0)
        self.assertEqual(result['name'], 'TESTING')

    def test_delete_company_hsa_plan_success(self):
        response = self.client.get(reverse('company_hsa_plan_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(len(array), 1)

        response = self.client.delete(reverse('company_hsa_plan_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_hsa_plan_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(len(array), 0)
