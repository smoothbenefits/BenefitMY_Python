from datetime import date

from trigger_not_complete_enrollment_base import TriggerNotCompleteEnrollmentBase


class TriggerCompanyNotCompleteEnrollment(TriggerNotCompleteEnrollmentBase):
    def __init__(self):
        super(TriggerCompanyNotCompleteEnrollment, self).__init__()

    def _check_schedule(self, start_date):
        if (not start_date):
            return False

        date_diff = (start_date - date.today()).days

        # Current schedule settings:
        #  - only check and trigger this on the 5th day after
        #    the start date
        if (date_diff == -5):
            return True
        return False
