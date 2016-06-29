import responses
import copy
import datetime

from django.core.urlresolvers import reverse
from test_mock_time_tracking_app_base import TestMockTimeTrackingAppBase

class CompanyUserTimePunchCardReportTests(TestMockTimeTrackingAppBase):

    @responses.activate
    def test_get_time_punchcard_report_success(self):
        week_start_date = datetime.date(2016, 3, 13)
        week_end_date = datetime.date(2016, 3, 20)
        mock_url = self._setup_mock_url(week_start_date, week_end_date, 1)
        mock_json = self._setup_mock_return_json([week_start_date], 1, 3)
        self.setup_mock_get(
            path=mock_url,
            return_json = mock_json)
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_time_punch_card_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(1),
                                                'year': week_start_date.year,
                                                'month': week_start_date.month,
                                                'day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("Failed!")


    @responses.activate
    def test_get_worktime_report_success_no_timetracking_data(self):
        week_start_date = datetime.date(2016, 3, 13)
        week_end_date = datetime.date(2016, 3, 20)
        mock_url = self._setup_mock_url(week_start_date, week_end_date, 1)
        mock_json = []
        self.setup_mock_get(
            path=mock_url,
            return_json = mock_json,
            return_status = 404)
        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_time_punch_card_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(1),
                                                'year': week_start_date.year,
                                                'month': week_start_date.month,
                                                'day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
        else:
            self.assertFalse("Failed")

    def test_get_worktime_report_wrong_company(self):
        week_start_date = datetime.date(2016, 3, 13)

        if self.client.login(username='user2@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_time_punch_card_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(144),
                                                'year': week_start_date.year,
                                                'month': week_start_date.month,
                                                'day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 403)
        else:
            self.assertFalse("Failed")

    def test_get_worktime_report_non_admin(self):
        week_start_date = datetime.date(2016, 3, 13)

        if self.client.login(username='user3@benefitmy.com', password='foobar'):
            response = self.client.get(reverse('company_time_punch_card_report_weekly',
                                               kwargs={
                                                'pk': self.normalize_key(144),
                                                'year': week_start_date.year,
                                                'month': week_start_date.month,
                                                'day': week_start_date.day}))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 403)
        else:
            self.assertFalse("Failed")
