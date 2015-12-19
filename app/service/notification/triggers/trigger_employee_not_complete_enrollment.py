from datetime import date

from trigger_not_complete_enrollment_base import TriggerNotCompleteEnrollmentBase


class TriggerEmployeeNotCompleteEnrollment(TriggerNotCompleteEnrollmentBase):
    def __init__(self):
        super(TriggerEmployeeNotCompleteEnrollment, self).__init__()

    def _check_schedule(self, start_date):
        if (not start_date):
            return False

        date_diff = (start_date - date.today()).days

        # Current schedule settings:
        #  - between 4 days before and 4 days after start date, send daily
        #  - prior to 4 days before start date, send one every 5 days
        #  - post 4 days after start date, stop notification
        if ((date_diff >= -4 and date_diff <= 4)
            or (date_diff > 4 and date_diff % 5 == 0)):
            return True
        return False
