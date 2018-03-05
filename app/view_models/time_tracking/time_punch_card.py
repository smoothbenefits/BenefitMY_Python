from app.service.hash_key_service import HashKeyService
from app.service.date_time_service import DateTimeService
from .time_card_validation_issue import TimeCardValidationIssue

# Time Punch Card Attribute Types
PUNCH_CARD_ATTRIBUTE_TYPE_STATE = 'State'
PUNCH_CARD_ATTRIBUTE_TYPE_PROJECT = 'Project'
PUNCH_CARD_ATTRIBUTE_TYPE_HOURLY_RATE = 'HourlyRate'

# Time Punch Card Types
PUNCH_CARD_TYPE_WORK_TIME = 'Work Time'
PUNCH_CARD_TYPE_COMPANY_HOLIDAY = 'Company Holiday'
PUNCH_CARD_TYPE_PAID_TIME_OFF = 'Paid Time Off'
PUNCH_CARD_TYPE_SICK_TIME = 'Sick Time'
PUNCH_CARD_TYPE_PERSONAL_LEAVE = 'Personal Leave'
PUNCH_CARD_TYPE_BREAK_TIME = 'Break Time'


class TimePunchCard(object):
    hash_key_service = HashKeyService()
    date_time_service = DateTimeService()

    def __init__(self, punch_card_domain_model):
        if (punch_card_domain_model is None):
            raise ValueError('Must pass valid time punch card domain model.')

        # List out instance variables
        self.user_id = None
        self.user_info = None
        self.date = None
        self.start = None
        self.end = None
        self.state = None
        self.card_type = None
        self.in_progress = None

        # Parse out user ID
        user_descriptor = punch_card_domain_model['employee']['personDescriptor']
        self.user_id = int(self.hash_key_service.decode_key_with_environment(user_descriptor))

        # Parse card type
        self.card_type = punch_card_domain_model.get('recordType')

        # Parse all dates and times to objects
        self.date = self.date_time_service.parse_date_time(punch_card_domain_model['date'])

        start_str = punch_card_domain_model.get('start')
        if (start_str):
            self.start = self.date_time_service.parse_date_time(start_str)

        end_str = punch_card_domain_model.get('end')
        if (end_str):
            self.end = self.date_time_service.parse_date_time(end_str)

        # Parse attributes
        attributes = punch_card_domain_model.get('attributes')
        if (attributes):
            for attribute in attributes:
                # For now only cares about state
                if attribute['name'] == PUNCH_CARD_ATTRIBUTE_TYPE_STATE:
                    self.state = attribute['value']
                    break

        in_progress_str = punch_card_domain_model.get('inProgress')
        if (in_progress_str):
            self.in_progress = bool(in_progress_str)

        # Support lasy-evaluated validation
        self._validation_issues = None

    def get_punch_card_hours(self):
        raw_hours = self.__get_raw_card_hours()
        if self.card_type == PUNCH_CARD_TYPE_BREAK_TIME:
            return -raw_hours
        return raw_hours

    def __get_raw_card_hours(self):
        if (self.start is not None and self.end is not None):
            card_hours = self.date_time_service.get_time_diff_in_hours(self.start, self.end, 2)
            return card_hours 
        return 0.0

    def get_card_day_of_week_iso(self):
        return self.date.isoweekday() % 7

    @property
    def validation_issues(self):
        if (self._validation_issues is None):
            self._validation_issues = self._validate() 
        
        return self._validation_issues

    def is_valid(self):
        issues = self.validation_issues
        blocking_issue = next(
            (issue for issue in issues if issue.level > TimeCardValidationIssue.LEVEL_WARNING),
            None)
        return blocking_issue is None

    def _validate(self):
        validation_issues = []

        card_hours = self.__get_raw_card_hours()

        # 1. Unclosed timecard (clocked in, but not out)
        if ((self.start is not None and self.end is None)
            or (self.in_progress)):
            validation_issues.append(TimeCardValidationIssue(
                TimeCardValidationIssue.LEVEL_ERROR,
                '[Unclosed Card] Clocked in, but not out, by midnight.'))

        # 2. Negative hours
        if (card_hours < 0.0):
            validation_issues.append(TimeCardValidationIssue(
                TimeCardValidationIssue.LEVEL_ERROR,
                '[Invalid Card Balance] Card with negative accounted hours.'))

        # 3. Long working hours, such as over 10 hours work
        if (card_hours >= 10.0):
            validation_issues.append(TimeCardValidationIssue(
                TimeCardValidationIssue.LEVEL_WARNING,
                '[Unusual Card Balance] Card with more than 10 hours.'))
        
        return validation_issues
