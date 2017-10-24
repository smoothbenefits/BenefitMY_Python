from django.contrib.auth import get_user_model
from app.service.date_time_service import DateTimeService
from .time_card_validation_issue import TimeCardValidationIssue
from ..user_info import UserInfo

User = get_user_model()


''' View model to represent the aggregate of all time cards
    filed for an employee in a day. 
'''
class EmployeeDailyPunchCardAggregate(object):
    date_time_service = DateTimeService()

    def __init__(self, employee_user_id, date):

        # List out instance variables
        self.user_id = employee_user_id
        self.user_info = None
        self.date = date
        self._time_punch_cards = []

        if (self.user_id):
            user_model = User.objects.get(pk=self.user_id)
            self.user_info = UserInfo(user_model)

        # Support lasy-evaluated validation
        self._validation_issues = None

    @property
    def validation_issues(self):
        if (self._validation_issues is None):
            self._validation_issues = self._validate() 
        
        return self._validation_issues

    def _validate(self):
        validation_issues = []

        [validation_issues.extend(card.validation_issues) for card in self._time_punch_cards]

        # Aggregate specific validations
        hours = self.get_total_hours()

        ## 1.Long working hours in a day, such as over 10 hours work
        if (hours >= 10.0):
            validation_issues.append(TimeCardValidationIssue(
                TimeCardValidationIssue.LEVEL_WARNING,
                '[Unusual Daily Balance] More than 10 total hours filed in a day.'))

        return validation_issues

    def get_total_hours(self):
        return sum(card.get_punch_card_hours() for card in self._time_punch_cards)

    @property
    def employee_full_name(self):
        if (self.user_info is None):
            return None
        return self.user_info.full_name

    def add_card(self, time_punch_card):
        self._time_punch_cards.append(time_punch_card)
