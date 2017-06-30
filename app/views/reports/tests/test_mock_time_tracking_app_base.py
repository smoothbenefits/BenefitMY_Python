import copy
import responses

from django.test import TestCase
from django.conf import settings
from app.views.tests.view_test_base import ViewTestBase
from app.views.tests.mock_timetracking_app import TimeTrackingAppMock

class TestMockTimeTrackingAppBase(TestCase, ViewTestBase, TimeTrackingAppMock):
    # your fixture files here
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user',
                'sys_application_feature', '34_company_user', 'company_features',
                '79_company_department', '82_company_job', '83_company_division',
                'employee_profile', '27_compensation_update_reason',
                '50_employee_compensation', '74_phraseology', '76_employee_phraseology']

    def _setup_mock_url(self, start_week_start_date, end_week_start_date, company_id):
        timetracking_service_path = 'api/v1/company/{0}/work_timesheets?start_date={1}&end_date={2}'.format(
            '{0}_{1}'.format(settings.ENVIRONMENT_IDENTIFIER, self.normalize_key(company_id)),
            start_week_start_date.isoformat(),
            end_week_start_date.isoformat())
        return timetracking_service_path

    def _setup_mock_return_json(self, week_start_dates, company_id, user_id):
        worksheets = []
        for start_date in week_start_dates:
            worksheets.append(self._get_mock_single_week_weektime(start_date, company_id, user_id))
        return worksheets

    def _get_mock_single_week_weektime(self, week_start_date, company_id, user_id):
        timecard_1 = copy.deepcopy(self.WORKTIME_CARD_ITEM_BASE)
        worksheet = copy.deepcopy(self.WORKTIME_SHEET_RESPONSE_ITEM_BASE)
        worksheet['employee']['personDescriptor'] = '{0}_{1}'.format(
            settings.ENVIRONMENT_IDENTIFIER,
            self.normalize_key(user_id))
        worksheet['employee']['companyDescriptor'] = '{0}_{1}'.format(
            settings.ENVIRONMENT_IDENTIFIER,
            self.normalize_key(company_id))
        worksheet['weekStartDate'] = week_start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        worksheet['timecards'].append(timecard_1)
        return worksheet
