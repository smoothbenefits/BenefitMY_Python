from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import MULTIPART_CONTENT
from view_test_base import ViewTestBase
from app.service.application_feature_service import (
    APP_FEATURE_INTERNAL_TESTDEFAULTON,
    APP_FEATURE_INTERNAL_TESTDEFAULTOFF
)
import json


class CompanyUserFeaturesTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['49_period_definition', '10_company', 'sys_application_feature',
                '23_auth_user', '34_company_user', '81_company_user_features']

    def test_get_defaultoverridenwithdifferentvalue_receiveoverridevalue(self):
        response = self.client.get(reverse('company_user_all_features_api',
                                           kwargs={
                                                'company_id': self.normalize_key(1),
                                                'user_id': self.normalize_key(2)
                                           }))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertTrue(APP_FEATURE_INTERNAL_TESTDEFAULTON in result)
        self.assertEqual(result[APP_FEATURE_INTERNAL_TESTDEFAULTON], False)

    def test_get_defaultnotoverriden_receivedefaultvalue(self):
        response = self.client.get(reverse('company_user_all_features_api',
                                           kwargs={
                                                'company_id': self.normalize_key(1),
                                                'user_id': self.normalize_key(2)
                                           }))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertTrue(APP_FEATURE_INTERNAL_TESTDEFAULTOFF in result)
        self.assertEqual(result[APP_FEATURE_INTERNAL_TESTDEFAULTOFF], False)

    def test_get_defaultoverridenwithsamevalue_receivedefaultvalue(self):
        response = self.client.get(reverse('company_user_all_features_api',
                                           kwargs={
                                                'company_id': self.normalize_key(1),
                                                'user_id': self.normalize_key(3)
                                           }))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), dict)

        self.assertTrue(APP_FEATURE_INTERNAL_TESTDEFAULTON in result)
        self.assertEqual(result[APP_FEATURE_INTERNAL_TESTDEFAULTON], True)
