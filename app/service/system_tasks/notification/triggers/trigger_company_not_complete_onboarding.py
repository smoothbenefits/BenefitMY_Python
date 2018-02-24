from datetime import date

from trigger_not_complete_onboarding_base import TriggerNotCompleteOnboardingBase

TERMINATE_NOTIFICATION_DAY = 30


class TriggerCompanyNotCompleteOnboarding(TriggerNotCompleteOnboardingBase):
    def __init__(self):
        super(TriggerCompanyNotCompleteOnboarding, self).__init__()

    def _check_schedule(self, start_date):
        if (not start_date):
            return False

        # Document creation should always be earlier than or the same as today
        date_diff = (date.today() - start_date).days

        # Current schedule settings:
        #  - 30 days after employment start date, send notification to employer
        if (date_diff == TERMINATE_NOTIFICATION_DAY):
            return True

        return False
