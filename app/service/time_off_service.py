from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

from app.service.hash_key_service import HashKeyService
from app.service.web_request_service import WebRequestService
from app.view_models.time_tracking.time_off_record import TimeOffRecord
from app.view_models.time_tracking.employee_time_off_record_aggregate import EmployeeTimeOffRecordAggregate

User = get_user_model()

# Supported time off types
TIME_OFF_TYPE_PTO = 'Paid Time Off (PTO)'
TIME_OFF_TYPE_SICKTIME = 'Sick Time'

# Expected time off status
TIME_OFF_STATUS_APPROVED = 'APPROVED' 
TIME_OFF_STATUS_DENIED = 'DENIED'
TIME_OFF_STATUS_REVOKED = 'REVOKED'
TIME_OFF_STATUS_PENDING = 'PENDING'
TIME_OFF_STATUS_CANCELED = 'CANCELED'


class TimeOffService(object):

    hash_key_service = HashKeyService()
    request_service = WebRequestService()

    def get_company_users_time_off_records_by_date_range(
        self,
        company_id,
        start_date,
        end_date
    ):
        user_records = []
        api_url = '{0}api/v1/company/{1}/timeoffs?start_date={2}&end_date={3}'.format(
            settings.TIME_TRACKING_SERVICE_URL,
            self.hash_key_service.encode_key_with_environment(company_id),
            start_date.isoformat(),
            end_date.isoformat())

        r = self.request_service.get(api_url)
        if r.status_code == 404:
            return user_records

        r.raise_for_status()

        all_entries = r.json()
        for entry in all_entries:
            user_records.append(TimeOffRecord(entry))

        # Sort the records by user ID
        sorted_records = sorted(user_records, key=lambda record: (record.requestor_user_id, record.start_date_time))

        return sorted_records

    def get_company_users_time_off_record_aggregates_by_date_range(
        self,
        company_id,
        start_date,
        end_date
    ):
        mappings = {}

        all_records = self.get_company_users_time_off_records_by_date_range(company_id, start_date, end_date)
        for record in all_records:
            if record.requestor_user_id not in mappings:
                mappings[record.requestor_user_id] = EmployeeTimeOffRecordAggregate(record.requestor_user_id)
            mappings[record.requestor_user_id].add_record(record)

        unsorted = mappings.values()
        return sorted(unsorted, key=lambda aggregate: aggregate.user_id)
