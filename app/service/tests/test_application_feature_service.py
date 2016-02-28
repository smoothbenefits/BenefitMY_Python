from django.test import TestCase
from app.service.application_feature_service import ApplicationFeatureService

# Create your tests here.
class TestApplicationFeatureService(TestCase):

    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user', '13_benefit_type',
                '17_supplemental_life_insurance_condition', '15_benefit_policy_key',
                '16_benefit_policy_type', 'sys_application_feature', 'company_features', 
                '14_document_type', '34_company_user', '34_document', '25_signature']

    def test_get_company_list_with_feature_enabled(self):
        service = ApplicationFeatureService()

        result = service.get_company_list_with_feature_enabled('FSA')
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)

        result = service.get_company_list_with_feature_enabled('DD')
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertIn(1, result)

        result = service.get_company_list_with_feature_enabled('BasicLife')
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 0)

    def test_get_company_list_with_feature_disabled(self):
        service = ApplicationFeatureService()

        result = service.get_company_list_with_feature_disabled('DentalBenefit')
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertIn(2, result)

        result = service.get_company_list_with_feature_disabled('DD')
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 0)
