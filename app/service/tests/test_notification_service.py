# test document
# tests can be kicked off by running "python manage.py test app/tests/"
from django.test import TestCase
from app.service.notification.triggers.trigger_employee_not_sign_document \
	import TriggerEmployeeNotSignDocument

import re

# Create your tests here.
class TestNotificationService(TestCase):

	fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user', '13_benefit_type',
                '17_supplemental_life_insurance_condition', '15_benefit_policy_key',
                '16_benefit_policy_type', 'sys_application_feature', '14_document_type',
                '21_benefit_plan', '22_benefit_details', '26_supplemental_life_insurance',
                '31_company_benefit_plan_option', '32_enrolled', '34_company_user',
                '37_fsa_plan', '38_supplemental_life_rate', '39_company_supplement_life_insurance',
                '41_user_company_benefit_plan_option', '42_company_fsa', '43_fsa',
                '44_person_company_suppl_life', '45_suppl_life_beneficiary', '46_hra_plan',
                '47_company_hra_plan', '48_person_company_hra_plan', 'company_features',
                'life_insurance', 'ltd_insurance', 'std_insurance', 'waived_benefit']

	''' encode a 'None' key, should return None
	'''
	def test_Encode_NoneKey_None(self):
		trigger = TriggerEmployeeNotSignDocument()
		result = trigger._examine_condition()
		#self.assertEqual(result, True)
		# assert False
