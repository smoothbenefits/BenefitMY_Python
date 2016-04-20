import json
import responses
import copy
import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from app.views.tests.view_test_base import ViewTestBase
from app.views.tests.mock_timetracking_app import TimeTrackingAppMock

class CompanyUserWorktimeReportTests(TestCase, ViewTestBase, TimeTrackingAppMock):
    # your fixture files here
    fixtures = ['24_person', '49_period_definition', '10_company', '23_auth_user',
                'sys_application_feature', '34_company_user', 'company_features',
                'employee_profile', '27_compensation_update_reason', '50_employee_compensation']


    def _setup_mock_url(self, week_start_date, company_id):
        timetracking_service_path = 'api/v1/company/{0}/work_timesheets?start_date={1}&end_date={1}'.format(
            '{0}_{1}'.format(settings.ENVIRONMENT_IDENTIFIER, self.normalize_key(company_id)),
            week_start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            week_start_date.strftime('%Y-%m-%dT%H:%M:%S'))
        return timetracking_service_path

    def _setup_mock_return_json(self, week_start_date, company_id, user_id):
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
        return [worksheet]

    @responses.activate
    def test_get_worktime_report_success(self):
        week_start_date = datetime.date(2016, 3, 13)
        mock_url = self._setup_mock_url(week_start_date, 1)
        mock_json = self._setup_mock_return_json(week_start_date, 1, 3)
        self.setup_mock_get(
            path=mock_url,
            return_json = mock_json)
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_worktime_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(1),
                                                'from_year': week_start_date.year,
                                                'from_month': week_start_date.month,
                                                'from_day': week_start_date.day,
                                                'to_year': week_start_date.year,
                                                'to_month': week_start_date.month,
                                                'to_day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("Failed!")

    @responses.activate
    def test_get_worktime_report_success_no_timetracking_data(self):
        week_start_date = datetime.date(2016, 3, 13)
        mock_url = self._setup_mock_url(week_start_date, 1)
        mock_json = []
        self.setup_mock_get(
            path=mock_url,
            return_json = mock_json,
            return_status = 404)
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_worktime_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(1),
                                                'from_year': week_start_date.year,
                                                'from_month': week_start_date.month,
                                                'from_day': week_start_date.day,
                                                'to_year': week_start_date.year,
                                                'to_month': week_start_date.month,
                                                'to_day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("Failed")

    def test_get_worktime_report_wrong_company(self):
        week_start_date = datetime.date(2016, 3, 13)

        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_worktime_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(144),
                                                'from_year': week_start_date.year,
                                                'from_month': week_start_date.month,
                                                'from_day': week_start_date.day,
                                                'to_year': week_start_date.year,
                                                'to_month': week_start_date.month,
                                                'to_day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 403)
        else:
            self.assertFalse("Failed")

    def test_get_worktime_report_non_admin(self):
        week_start_date = datetime.date(2016, 3, 13)

        if self.client.login(username='user3@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_worktime_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(144),
                                                'from_year': week_start_date.year,
                                                'from_month': week_start_date.month,
                                                'from_day': week_start_date.day,
                                                'to_year': week_start_date.year,
                                                'to_month': week_start_date.month,
                                                'to_day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 403)
        else:
            self.assertFalse("Failed")
