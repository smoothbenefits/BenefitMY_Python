import requests

from django.conf import settings
from django.contrib.auth import get_user_model

from app.service.hash_key_service import HashKeyService

User = get_user_model()


class TimeTrackingService(object):

    def get_all_users_submitted_work_timesheet_by_week_start_date(self, week_start_date):
        users = []

        api_url = '{0}{1}?start_date={2}&end_date={2}'.format(
                        settings.TIME_TRACKING_SERVICE_URL,
                        'api/v1/work_timesheets',
                        week_start_date.isoformat())

        # Make the request and parse the response as json
        r = requests.get(api_url)
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

        hash_key_service = HashKeyService()
        decoded_str = hash_key_service.decode_key(hashed_id_part)

        if (decoded_str):
            return int(decoded_str)

        return decoded_str
