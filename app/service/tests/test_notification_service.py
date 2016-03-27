# test document
# tests can be kicked off by running "python manage.py test app/tests/"
from django.test import TestCase
from app.service.system_tasks.notification.triggers.trigger_employee_not_sign_document \
	import TriggerEmployeeNotSignDocument
from app.service.system_tasks.notification.triggers.trigger_company_not_sign_document \
	import TriggerCompanyNotSignDocument
from app.service.system_tasks.notification.actions.action_notify_company_not_sign_document \
	import ActionNotifyCompanyNotSignDocument
from app.service.system_tasks.notification.actions.action_notify_employee_not_sign_document \
	import ActionNotifyEmployeeNotSignDocument

# Create your tests here.
class TestNotificationService(TestCase):

	fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user', '13_benefit_type',
                '17_supplemental_life_insurance_condition', '15_benefit_policy_key',
                '16_benefit_policy_type', 'sys_application_feature', '14_document_type',
				'34_company_user', '34_document', '25_signature']

	''' encode a 'None' key, should return None
	'''
	def test_Trigger_Return_Correct_Condition(self):
		trigger = TriggerEmployeeNotSignDocument()
		trigger = TriggerCompanyNotSignDocument()
		# result = trigger._examine_condition()
		# self.assertEqual(result, True)

	def test_action_executed_correctly(self):
		action = ActionNotifyEmployeeNotSignDocument()
		action = ActionNotifyCompanyNotSignDocument()
		# user_list = {"company_user_id_list": { 1: [3]}}
		# action.execute(user_list)
		# assert False
