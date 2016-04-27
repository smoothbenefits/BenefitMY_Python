import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase


class CoiLienWaiverFormTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user', '13_benefit_type',
                '34_company_user']

    def test_get_coi_lien_waiver_form_success(self):
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('coi_lien_waiver_form_api',
                                               kwargs={}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("login failed!")
