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
            user_id = self._decode_environment_aware_id(user_descriptor)
            users.append(user_id)

        return users

    def _decode_environment_aware_id(self, encoded_id):
        if (not encoded_id):
            return None
        hashed_id_part = encoded_id.split('_', 1)[1]
        if (not hashed_id_part):
            return None

        decoded_str = self.hash_key_service.decode_key(hashed_id_part)

        if (decoded_str):
            return int(decoded_str)

        return decoded_str

    def _encode_environment_aware_id(self, id_to_encode):
        if (not id_to_encode):
            return None
        hash_id = self.hash_key_service.encode_key(id_to_encode)

        return '{0}_{1}'.format(settings.ENVIRONMENT_IDENTIFIER, hash_id)



    def get_company_users_submitted_work_timesheet_by_week_start_date(self, company_id, week_start_date):
        user_timesheets = []
        api_url = '{0}api/v1/company/{1}/work_timesheets?start_date={2}&end_date={2}'.format(
            settings.TIME_TRACKING_SERVICE_URL,
            self._encode_environment_aware_id(company_id),
            week_start_date.isoformat())

        r = self.request_service.get(api_url)
        if r.status_code == 404:
            return user_timesheets

        all_entries = r.json()
        for entry in all_entries:
            user_descriptor = entry['employee']['personDescriptor']
            user_id = self._decode_environment_aware_id(user_descriptor)
            item = copy.deepcopy(entry)
            item['user_id'] = user_id
            user_timesheets.append(item)

        return user_timesheets
