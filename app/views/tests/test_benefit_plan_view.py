from django.test import TestCase
from django.core.urlresolvers import reverse
import json


class BenefitPlanTestCase(TestCase):
    # your fixture files here
    fixtures = ['31_company_benefit_plan_option', '21_benefit_plan', '10_company', '13_benefit_type']

    def test_get_document_type(self):
        response = self.client.get(reverse('benefit_plan_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['benefit']['total_cost_per_period'], '678.87')
        self.assertEqual(result['benefit']['benefit_option_type'], 'individual')
        self.assertEqual(result['benefit']['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')



        response = self.client.get(reverse('benefit_plan_api',
                                           kwargs={'pk': 3}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result), dict)
        self.assertEqual(result['benefit']['total_cost_per_period'], '1024.45')
        self.assertEqual(result['benefit']['benefit_option_type'], 'individual_plus_children')
        self.assertEqual(result['benefit']['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')


class CompanyBenefitPlanTestCase(TestCase):
    # your fixture files here
    fixtures = ['31_company_benefit_plan_option', '21_benefit_plan', '10_company', '13_benefit_type']

    def test_get_document_type(self):
        response = self.client.get(reverse('company_benefit_plan_api',
                                           kwargs={'pk': 1}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(type(result['benefits']), list)
        self.assertEqual(result['benefits'][0]['total_cost_per_period'], '678.87')
        self.assertEqual(result['benefits'][0]['benefit_option_type'], 'individual')
        self.assertEqual(result['benefits'][0]['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')

        self.assertEqual(result['benefits'][2]['total_cost_per_period'], '1024.45')
        self.assertEqual(result['benefits'][2]['benefit_option_type'], 'individual_plus_children')
        self.assertEqual(result['benefits'][2]['benefit_plan']['name'], 'Blue Cross Blue Shield of Mass. HMO Blue')
