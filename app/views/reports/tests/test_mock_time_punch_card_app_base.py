import copy
import responses

from django.test import TestCase
from django.conf import settings
from app.views.tests.view_test_base import ViewTestBase
from app.views.tests.mock_time_punch_card_app import TimePunchCardAppMock


class TestMockTimePunchCardAppBase(TestCase, ViewTestBase, TimePunchCardAppMock):
    
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user',
                'sys_application_feature', '34_company_user', 'company_features',
                '79_company_department', '82_company_job', '83_company_division',
                'employee_profile', '27_compensation_update_reason',
                '50_employee_compensation', '74_phraseology', '76_employee_phraseology']

    def _setup_mock_url(self, start_date, end_date, company_id):
        service_path = 'api/v1/company/{0}/time_punch_cards?start_date={1}&end_date={2}'.format(
            '{0}_{1}'.format(settings.ENVIRONMENT_IDENTIFIER, self.normalize_key(company_id)),
            start_date.isoformat(),
            end_date.isoformat())
        return service_path

    def _setup_mock_return_json(self, week_start_dates, company_id, user_id):
        cards = []
        cards.append(copy.deepcopy(self.PUNCH_CARD_BASE))
        return cards
