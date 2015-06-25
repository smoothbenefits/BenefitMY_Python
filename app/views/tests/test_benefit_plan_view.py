from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class BenefitPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['31_company_benefit_plan_option', '21_benefit_plan', '10_company', '13_benefit_type']

    def test_get_benefit_plan_by_id(self):
        response = self.client.get(reverse('benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['benefit']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')
        self.assertEqual(result['benefit']['pcp_link'], 'https://www.bluecrossma.com/wps/portal/members/using-my-plan/doctors-hospitals/findadoctor/')



        response = self.client.get(reverse('benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['benefit']['name'], 'Aetna Dental')
        self.assertEqual(result['benefit']['pcp_link'], None)

    def test_benefit_plan_creation_success(self):
        benefit_data = {"benefit_type": "Medical",
                        "benefit_name": "TestMedical",
                        "mandatory_pcp": True,
                        "pcp_link": "http://www.bluecrossma.com"}

        response = self.client.post(reverse('benefit_post_api'), 
                                    data=json.dumps(benefit_data),
                                    content_type='application/json')

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.content)
        self.assertIn("benefit", result)
        created_benefit = result["benefit"]
        self.assertIn("id", created_benefit)
        self.assertEqual(created_benefit['name'], "TestMedical")
        self.assertEqual(created_benefit['benefit_type'], 1)
        self.assertEqual(created_benefit['mandatory_pcp'], True)
        self.assertEqual(created_benefit['pcp_link'], "http://www.bluecrossma.com")

    def test_benefit_plan_delete_success(self):
        response = self.client.delete(reverse('benefit_plan_api',
                                      kwargs={'pk': self.normalize_key(4)}))
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(4)}))
        self.assertEqual(response.status_code, 404)

class CompanyBenefitPlanTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['31_company_benefit_plan_option', '21_benefit_plan', '10_company', '13_benefit_type']

    def test_get_company_benefit_plan_by_id(self):
        response = self.client.get(reverse('company_benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result['benefits']), list)
        self.assertEqual(result['benefits'][0]['total_cost_per_period'], '678.87')
        self.assertEqual(result['benefits'][0]['benefit_option_type'], 'individual')
        self.assertEqual(result['benefits'][0]['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')
        self.assertEqual(result['benefits'][0]['benefit_plan']['pcp_link'], 'https://www.bluecrossma.com/wps/portal/members/using-my-plan/doctors-hospitals/findadoctor/')


        self.assertEqual(result['benefits'][2]['total_cost_per_period'], '1024.45')
        self.assertEqual(result['benefits'][2]['benefit_option_type'], 'individual_plus_children')
        self.assertEqual(result['benefits'][2]['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')
        self.assertEqual(result['benefits'][2]['benefit_plan']['pcp_link'], 'https://www.bluecrossma.com/wps/portal/members/using-my-plan/doctors-hospitals/findadoctor/')

