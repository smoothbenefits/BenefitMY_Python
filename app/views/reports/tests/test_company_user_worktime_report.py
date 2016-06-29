import responses
import copy
import datetime

from django.core.urlresolvers import reverse
from test_mock_time_tracking_app_base import TestMockTimeTrackingAppBase

class CompanyUserWorktimeReportTests(TestMockTimeTrackingAppBase):

    @responses.activate
    def test_get_single_worktime_report_success(self):
        week_start_date = datetime.date(2016, 3, 13)
        mock_url = self._setup_mock_url(week_start_date, week_start_date, 1)
        mock_json = self._setup_mock_return_json([week_start_date], 1, 3)
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
    def test_get_multiple_week_worktime_report_success(self):
        start_week_start_date = datetime.date(2016, 3, 13)
        end_week_start_date = datetime.date(2016, 3, 20)
        mock_url = self._setup_mock_url(start_week_start_date, end_week_start_date, 1)
        start_dates = [start_week_start_date, end_week_start_date]
        mock_json = self._setup_mock_return_json(start_dates, 1, 3)
        self.setup_mock_get(
            path=mock_url,
            return_json = mock_json)
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_worktime_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(1),
                                                'from_year': start_week_start_date.year,
                                                'from_month': start_week_start_date.month,
                                                'from_day': start_week_start_date.day,
                                                'to_year': end_week_start_date.year,
                                                'to_month': end_week_start_date.month,
                                                'to_day': end_week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("Failed!")

    @responses.activate
    def test_get_worktime_report_success_no_timetracking_data(self):
        week_start_date = datetime.date(2016, 3, 13)
        mock_url = self._setup_mock_url(week_start_date, week_start_date, 1)
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
