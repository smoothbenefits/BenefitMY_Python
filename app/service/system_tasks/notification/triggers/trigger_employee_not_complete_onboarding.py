from datetime import date

from trigger_not_complete_onboarding_base import TriggerNotCompleteOnboardingBase

DAILY_EMAIL_START_DAY = 23
TERMINATE_NOTIFICATION_DAY = 30
NOTIFICATION_INTERVAL = 5


class TriggerEmployeeNotCompleteOnboarding(TriggerNotCompleteOnboardingBase):
    def __init__(self):
        super(TriggerEmployeeNotCompleteOnboarding, self).__init__()

    def _check_schedule(self, start_date):
        if (not start_date):
            return False

        date_diff = (date.today() - start_date).days

        # Current schedule settings:
        #  - between 23 days after and 30 days after benefit start date, send daily
        #  - prior to 23 days after benefit start date, send one every 5 days
        #  - post 30 days after benefit start date, stop notification
        if ((date_diff >= DAILY_EMAIL_START_DAY and date_diff <= TERMINATE_NOTIFICATION_DAY)
            or (date_diff < DAILY_EMAIL_START_DAY and date_diff % NOTIFICATION_INTERVAL == 0)):
            return True
        return False
