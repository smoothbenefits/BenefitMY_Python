from app.service.hash_key_service import HashKeyService
from app.service.date_time_service import DateTimeService

# Time Punch Card Attribute Types
PUNCH_CARD_ATTRIBUTE_TYPE_STATE = 'State'
PUNCH_CARD_ATTRIBUTE_TYPE_PROJECT = 'Project'
PUNCH_CARD_ATTRIBUTE_TYPE_HOURLY_RATE = 'HourlyRate'


class TimePunchCard(object):
    hash_key_service = HashKeyService()
    date_time_service = DateTimeService()

    def __init__(self, punch_card_domain_model):
        if (punch_card_domain_model is None):
            raise ValueError('Must pass valid time punch card domain model.')

        # List out instance variables
        self.user_id = None
        self.date = None
        self.start = None
        self.end = None
        self.state = None
        self.card_type = None

        # Parse out user ID
        user_descriptor = punch_card_domain_model['employee']['personDescriptor']
        self.user_id = int(self.hash_key_service.decode_key_with_environment(user_descriptor))

        # Parse card type
        self.card_type = punch_card_domain_model['recordType']

        # Parse all dates and times to objects
        self.date = self.date_time_service.parse_date_time(punch_card_domain_model['date'])

        start_str = punch_card_domain_model['start']
        if (start_str):
            self.start = self.date_time_service.parse_date_time(start_str)

        end_str = punch_card_domain_model['end']
        if (end_str):
            self.end = self.date_time_service.parse_date_time(end_str)

        # Parse attributes
        attributes = punch_card_domain_model['attributes']
        if (attributes):
            for attribute in attributes:
                # For now only cares about state
                if attribute['name'] == PUNCH_CARD_ATTRIBUTE_TYPE_STATE:
                    self.state = attribute['value']
                    break

    def get_punch_card_hours(self):
        if (self.start is not None and self.end is not None):
            return self.date_time_service.get_time_diff_in_hours(self.start, self.end)

        return None

    def get_card_day_of_week_iso(self):
        return self.date.isoweekday() % 7
