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
        self.assertEqual(result['benefit']['total_cost_per_period'], '678.87')
        self.assertEqual(result['benefit']['benefit_option_type'], 'individual')
        self.assertEqual(result['benefit']['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')
        self.assertEqual(result['benefit']['benefit_plan']['pcp_link'], 'https://www.bluecrossma.com/wps/portal/members/using-my-plan/doctors-hospitals/findadoctor/')



        response = self.client.get(reverse('benefit_plan_api',
                                           kwargs={'pk': self.normalize_key(3)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['benefit']['total_cost_per_period'], '1024.45')
        self.assertEqual(result['benefit']['benefit_option_type'], 'individual_plus_children')
        self.assertEqual(result['benefit']['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')
        self.assertEqual(result['benefit']['benefit_plan']['pcp_link'], 'https://www.bluecrossma.com/wps/portal/members/using-my-plan/doctors-hospitals/findadoctor/')


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

