from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import MULTIPART_CONTENT
from view_test_base import ViewTestBase
import json


class CompanyFeaturesTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['49_period_definition', '10_company', 'company_features', 'sys_application_feature' , '23_auth_user']

    def test_get_company_features(self):
        response = self.client.get(reverse('company_features_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0]['feature_status'], True)
        self.assertEqual(result[0]['company_feature']['id'], self.normalize_key(1))
        self.assertEqual(result[0]['company'], self.normalize_key(1))

        self.assertEqual(result[1]['feature_status'], True)
        self.assertEqual(result[1]['company_feature']['id'], self.normalize_key(2))
        self.assertEqual(result[1]['company'], self.normalize_key(1))

    def test_delete_company_features(self):
        response = self.client.get(reverse('company_features_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(result[0]['feature_status'], True)
        self.assertEqual(result[0]['company_feature']['id'], self.normalize_key(1))
        self.assertEqual(result[0]['company'], self.normalize_key(1))

        self.assertEqual(result[1]['feature_status'], True)
        self.assertEqual(result[1]['company_feature']['id'], self.normalize_key(2))
        self.assertEqual(result[1]['company'], self.normalize_key(1))


        response = self.client.delete(reverse('company_features_api',
                                              kwargs={'pk': self.normalize_key(3)}))

        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse('company_features_api',
                                           kwargs={'pk': self.normalize_key(2)}))

        result = json.loads(response.content)

        self.assertEqual(type(result), list)
        self.assertEqual(result, [])
