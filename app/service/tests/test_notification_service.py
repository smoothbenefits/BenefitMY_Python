# test document
# tests can be kicked off by running "python manage.py test app/tests/"
from django.test import TestCase
from app.service.notification.triggers.trigger_employee_not_sign_document \
	import TriggerEmployeeNotSignDocument

import re

# Create your tests here.
class TestNotificationService(TestCase):


	''' encode a 'None' key, should return None
	'''
	def test_Encode_NoneKey_None(self):
		trigger = TriggerEmployeeNotSignDocument()
		result = trigger._examine_condition()
		print 'After examine'
		assert False
