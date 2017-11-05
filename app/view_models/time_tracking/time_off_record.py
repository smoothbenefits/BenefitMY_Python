from django.contrib.auth import get_user_model
from app.service.hash_key_service import HashKeyService
from app.service.date_time_service import DateTimeService
from ..user_info import UserInfo

User = get_user_model()


class TimeOffRecord(object):
    hash_key_service = HashKeyService()
    date_time_service = DateTimeService()

    def __init__(self, time_off_domain_model):
        if (time_off_domain_model is None):
            raise ValueError('Must pass valid time off domain model.')

        # List out instance variables
        self.requestor_user_id = None
        self.requestor_user_info = None
        self.approver_user_id = None
        self.approver_user_info = None
        self.start_date_time = None
        self.duration = None
        self.status = None
        self.decision_timestamp = None
        self.record_type = None
        self.request_timestamp = None

        # Parse requestor info
        requestor_user_descriptor = time_off_domain_model['requestor']['personDescriptor']
        self.requestor_user_id = int(self.hash_key_service.decode_key_with_environment(requestor_user_descriptor))
        if (self.requestor_user_id):
            user_model = User.objects.get(pk=self.requestor_user_id)
            self.requestor_user_info = UserInfo(user_model)

        # Parse approver info
        if ('approver' in time_off_domain_model
            and time_off_domain_model['approver']):
            approver_user_descriptor = time_off_domain_model['approver']['personDescriptor']
            self.approver_user_id = int(self.hash_key_service.decode_key_with_environment(approver_user_descriptor))
            if (self.approver_user_id):
                user_model = User.objects.get(pk=self.approver_user_id)
                self.approver_user_info = UserInfo(user_model)

        # Parse record type
        self.record_type = time_off_domain_model['type']

        # Parse Duration
        self.duration = float(time_off_domain_model['duration'])

        # Parse status
        self.status = time_off_domain_model['status']

        # Parse all dates and times to objects
        self.start_date_time = self.date_time_service.parse_date_time(time_off_domain_model['startDateTime'])
        self.request_timestamp = self.date_time_service.parse_date_time(time_off_domain_model['requestTimestamp'])

        decision_time_str = time_off_domain_model['decisionTimestamp']
        if (decision_time_str):
            self.decision_timestamp = self.date_time_service.parse_date_time(decision_time_str)

    @property
    def requestor_full_name(self):
        if (self.requestor_user_info is None):
            return None
        return self.requestor_user_info.full_name

    @property
    def approver_full_name(self):
        if (self.approver_user_info is None):
            return None
        return self.approver_user_info.full_name 
