import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase


class SysApplicationFeatureTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['sys_application_feature']
    def test_get_sys_application_feature_set_success(self):
        response = self.client.get(reverse('sys_application_feature_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)

    def test_post_sys_application_feature_set_failed(self):
        new_feature = {'feature':'TestFeature'}
        response = self.client.post(reverse('sys_application_feature_api'),
                                    data=json.dumps(new_feature),
                                    content_type='application/json')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('sys_application_feature_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)

    def test_delete_sys_application_feature_set_failed(self):
        response = self.client.delete(reverse('sys_application_feature_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('sys_application_feature_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
