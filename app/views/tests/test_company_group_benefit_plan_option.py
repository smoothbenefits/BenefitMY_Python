import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class CompanyGroupBenefitPlanOptionTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['49_period_definition', '15_benefit_policy_key','10_company', '23_auth_user',
                '16_benefit_policy_type', '21_benefit_plan', '22_benefit_details',
                '13_benefit_type', '31_company_benefit_plan_option',
                '24_person', '61_company_group', '62_company_group_member',
                '66_company_group_benefit_plan_option']

    def test_get_company_group_benefit_plan_option_by_company_group_success(self):
        response = self.client.get(reverse('company_group_benefit_plan_option_api',
                                           kwargs={'company_group_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 4)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_group']['id'], self.normalize_key(1))

    def test_get_company_group_benefit_plan_option_by_non_exist_company_group_success_empty_list(self):
        response = self.client.get(reverse('company_group_benefit_plan_option_api',
                                           kwargs={'company_group_id': self.normalize_key(100000)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 0)

    def test_get_company_group_benefit_plan_option_by_company_plan_option_success(self):
        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 2)
        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_benefit_plan_option']['id'], self.normalize_key(4))

    def test_get_company_group_benefit_plan_option_by_non_exist_company_plan_option_failure(self):
        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(100000)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    def test_delete_company_group_benefit_plan_options_by_company_plan_option_success(self):
        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 2)

        response = self.client.delete(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                              kwargs={'pk': self.normalize_key(4)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 0)

    def test_post_company_group_benefit_plan_options_by_company_plan_option_success(self):
        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 2)

        post_data = [
            {
                'company_benefit_plan_option': self.normalize_key(4),
                'company_group': self.normalize_key(3)
            }
        ]

        response = self.client.post(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                            kwargs={'pk': self.normalize_key(4)}),
                                            data=json.dumps(post_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 3)

    def test_put_company_group_benefit_plan_options_by_company_plan_option_success(self):
        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 2)

        post_data = [
            {
                'company_benefit_plan_option': self.normalize_key(4),
                'company_group': self.normalize_key(2)
            }
        ]

        response = self.client.put(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                            kwargs={'pk': self.normalize_key(4)}),
                                            data=json.dumps(post_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_group_benefit_plan_option_by_company_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        array = json.loads(response.content)
        self.assertEqual(type(array), list)
        self.assertEqual(len(array), 1)

        result = array[0]
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company_group']['id'], self.normalize_key(2))
        self.assertEqual(result['company_benefit_plan_option']['id'], self.normalize_key(4))
