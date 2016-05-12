import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class PhraseologyViewTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['74_phraseology', '75_company_phraseology', 
                '49_period_definition', '10_company',
                '24_person', '23_auth_user']

    def test_get_all_phraseologys(self):
        response = self.client.get(reverse('all_phraseology_api'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 10)
