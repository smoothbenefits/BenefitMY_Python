import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class SysBenefitUpdateReasonTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['sys_benefit_update_reason', 'sys_benefit_update_reason_category']
    def test_get_sys_benefit_update_reason_success(self):
        response = self.client.get(reverse('sys_benefit_update_reason_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        print result
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
