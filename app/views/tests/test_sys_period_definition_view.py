import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class SysPeriodDefinitionTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['49_period_definition']
    def test_get_sys_period_definition_set_success(self):
        response = self.client.get(reverse('sys_period_definition_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 6)

    def test_post_sys_period_definition_set_failed(self):
        new_def = {'name':'TestPeriod', 'month_factor': 199}
        response = self.client.post(reverse('sys_period_definition_api'),
                                    data=json.dumps(new_def),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('sys_period_definition_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 6)

    def test_delete_sys_period_definition_set_failed(self):
        response = self.client.delete(reverse('sys_period_definition_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('sys_period_definition_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 6)
