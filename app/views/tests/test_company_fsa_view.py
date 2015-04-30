from django.test import TestCase
from django.core.urlresolvers import reverse
from view_test_base import ViewTestBase
import json


class FsaTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['37_fsa_plan', '23_auth_user', '24_person', '10_company', '42_company_fsa']

    def test_get_company_fsa(self):
        response = self.client.get(reverse('company_fsa_api',
                                           kwargs={'pk': self.normalize_key(1)}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)
        self.assertEqual(type(result[0]), dict)
        self.assertEqual(result[0]['fsa_plan']['id'], self.normalize_key(2))


