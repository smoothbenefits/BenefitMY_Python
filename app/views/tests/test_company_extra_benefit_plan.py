import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class CompanyExtraBenefitPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['56_company_extra_benefit_plan', '57_extra_benefit_item',
                '58_person_company_extra_benefit_plan', '59_person_company_extra_benefit_plan_item',
                '49_period_definition', '10_company', '24_person', '23_auth_user']

    def test_get_company_extra_benefit_plan(self):
        response = self.client.get(reverse('company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(1))
        self.assertEqual(len(result['benefit_items']), 2)

    def test_get_company_extra_benefit_plan_by_company(self):
        response = self.client.get(reverse('company_extra_benefit_plan_by_company_api',
                                           kwargs={'company_id': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['company'], self.normalize_key(1))
        self.assertEqual(len(result[0]['benefit_items']), 2)

    def test_delete_company_extra_benefit_plan(self):
        response = self.client.get(reverse('company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('company_extra_benefit_plan_api',
                                              kwargs={'pk': self.normalize_key(1)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 204)

        response = self.client.get(reverse('company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertEqual(result['detail'], 'Not found')

    def test_post_company_extra_benefit_plan(self):
        post_data = {"company": 2,
                     "description": "Test extra benefit plan",
                     "benefit_items": [
                        {
                            "name": "New Test IRA",
                            "description": "This is new test IRA"
                        },
                        {
                            "name": "New Test IRA 2",
                            "description": "This is new test IRA 2"
                        },
                        {
                            "name": "New Test IRA 3",
                            "description": "This is new test IRA 3"
                        }
                     ]
                    }
        response = self.client.post(reverse('company_extra_benefit_plan_api',
                                            kwargs={'pk': self.normalize_key(3)}),
                                            data=json.dumps(post_data),
                                            content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('company_extra_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['company'], self.normalize_key(2))

        key = result['id']
        response = self.client.get(reverse('company_extra_benefit_plan_api',
                                           kwargs={'pk': key}))
        result = json.loads(response.content)
        self.assertIsNotNone(response)
        self.assertEqual(result['company'], self.normalize_key(2))
        self.assertEqual(len(result['benefit_items']), 3)
