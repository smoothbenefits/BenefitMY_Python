from datetime import date

from trigger_not_complete_enrollment_base import TriggerNotCompleteEnrollmentBase

TERMINATE_NOTIFICATION_DAY = 30


class TriggerCompanyNotCompleteEnrollment(TriggerNotCompleteEnrollmentBase):
    def __init__(self):
        super(TriggerCompanyNotCompleteEnrollment, self).__init__()

    def _check_schedule(self, start_date):
        if (not start_date):
            return False

        # Document creation should always be earlier than or the same as today
        date_diff = (date.today() - start_date).days

        # Current schedule settings:
        #  - 30 days after benefit start date, send notification to employer
        if (date_diff == TERMINATE_NOTIFICATION_DAY):
            return True

        return False
