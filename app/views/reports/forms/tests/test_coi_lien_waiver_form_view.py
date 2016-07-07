import json
import responses

from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase
from app.views.tests.mock_coi_app import \
    CertificateOfInsuranceAppMock


class CoiLienWaiverFormTestCase(TestCase, ViewTestBase, CertificateOfInsuranceAppMock):
    # your fixture files here
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user', '13_benefit_type',
                '34_company_user']

    @responses.activate
    def test_get_coi_lien_waiver_form_success(self):
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            # Setup mock response for COI service call 
            contractor_id = '123abc'
            coi_path = 'api/v1/contractor/' + contractor_id
            mock_response_json = {
                '_id': contractor_id,
                'name': 'Test Contractor'
            }
            self.setup_mock_get(
                path=coi_path,
                return_json = mock_response_json)

            response = self.client.get(reverse('coi_lien_waiver_form_api',
                                               kwargs={
                                                'company_id': self.normalize_key(1),
                                                'contractor_id': contractor_id
                                                }))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("login failed!")
