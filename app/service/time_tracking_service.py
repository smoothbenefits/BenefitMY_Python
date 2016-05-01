import urlparse
import copy

from django.conf import settings
from django.contrib.auth import get_user_model

from app.service.hash_key_service import HashKeyService
from app.service.web_request_service import WebRequestService

User = get_user_model()


API_URL_WORK_TIMESHEET = '{0}{1}'.format(
    settings.TIME_TRACKING_SERVICE_URL,
    'api/v1/work_timesheets'
)


class TimeTrackingService(object):

    hash_key_service = HashKeyService()
    request_service = WebRequestService()

    def get_all_users_submitted_work_timesheet_by_week_start_date(self, week_start_date):
        users = []

        api_url = '{0}?start_date={1}&end_date={1}'.format(
                        API_URL_WORK_TIMESHEET,
                        week_start_date.isoformat())

        # Make the request and parse the response as json
        r = self.request_service.get(api_url)
        all_entries = r.json()

        for entry in all_entries:
            user_descriptor = entry['employee']['personDescriptor']
            user_id = int(hash_key_service.decode_key_with_environment(user_descriptor))
            users.append(user_id)

        return users

    def get_company_users_submitted_work_timesheet_by_week_range(
        self,
        company_id,
        start_week_start_date,
        end_week_start_date
    ):
        hash_key_service = HashKeyService()

        week_user_timesheets = {}
        api_url = '{0}api/v1/company/{1}/work_timesheets?start_date={2}&end_date={3}'.format(
            settings.TIME_TRACKING_SERVICE_URL,
            hash_key_service.encode_key_with_environment(company_id),
            start_week_start_date.isoformat(),
            end_week_start_date.isoformat())

        r = self.request_service.get(api_url)
        if r.status_code == 404:
            return week_user_timesheets

        all_entries = r.json()
        for entry in all_entries:
            user_descriptor = entry['employee']['personDescriptor']
            user_id = hash_key_service.decode_key_with_environment(user_descriptor)
            item = copy.deepcopy(entry)
            item['user_id'] = user_id

            # Group returned timesheet by work start date
            week_start_date = entry['weekStartDate']
            if week_start_date in week_user_timesheets:
                week_user_timesheets[week_start_date].append(item)
            else:
                week_user_timesheets[week_start_date] = [item]

        return week_user_timesheets
