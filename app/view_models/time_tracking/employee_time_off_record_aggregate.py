from django.contrib.auth import get_user_model
from app.service.date_time_service import DateTimeService
from ..user_info import UserInfo

User = get_user_model()


''' View model to represent the aggregate of a series of 
    time off records of a specific employee 
'''
class EmployeeTimeOffRecordAggregate(object):
    date_time_service = DateTimeService()

    def __init__(self, employee_user_id):

        # List out instance variables
        self.user_id = employee_user_id
        self.user_info = None
        self._time_off_records = []
        self._time_off_records_type_mapping = {}
        self._time_off_records_status_mapping = {}

        if (self.user_id):
            user_model = User.objects.get(pk=self.user_id)
            self.user_info = UserInfo(user_model)

    @property
    def employee_full_name(self):
        if (self.user_info is None):
            return None
        return self.user_info.full_name

    @property
    def all_records(self):
        return self._time_off_records

    def add_record(self, time_off_record):
        self._time_off_records.append(time_off_record)

        # Also categorize the record into the mapping keyed off record type
        record_type = time_off_record.record_type
        if (record_type not in self._time_off_records_type_mapping):
            self._time_off_records_type_mapping[record_type] = []
        self._time_off_records_type_mapping[record_type].append(time_off_record)

        # Also categorize the record into the mapping keyed off record status
        status = time_off_record.status
        if (status not in self._time_off_records_status_mapping):
            self._time_off_records_status_mapping[status] = []
        self._time_off_records_status_mapping[status].append(time_off_record)

    def get_records_by_type(self, record_type):
        if (record_type not in self._time_off_records_type_mapping):
            return []
        return self._time_off_records_type_mapping[record_type]

    def get_total_hours_by_record_type(self, record_type):
        if (record_type not in self._time_off_records_type_mapping):
            return 0.0
        return self.__calculate_total_hours(self.get_records_by_type(record_type))

    def get_records_by_status(self, record_status):
        if (record_status not in self._time_off_records_status_mapping):
            return []
        return self._time_off_records_status_mapping[record_status]

    def get_total_hours_by_record_status(self, record_status):
        if (record_status not in self._time_off_records_status_mapping):
            return 0.0
        return self.__calculate_total_hours(self.get_records_by_status(record_status))

    def __calculate_total_hours(self, record_list):
        return sum(record.duration for record in record_list)
