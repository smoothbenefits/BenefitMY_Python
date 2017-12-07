import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class SsnFormatCorrectionViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['85_person_ssn_correction',
                '49_period_definition',
                '10_company',
                '23_auth_user']

    def test_correct_for_all_success(self):
        response = self.client.get(reverse('ssn_format_correction_for_all_api',
                                           kwargs={}))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 2)
