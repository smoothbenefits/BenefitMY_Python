from datetime import date
from trigger_i9_expiration_base import TriggerI9ExpirationBase

EMAIL_START_DAY = 28
TERMINATE_NOTIFICATiON_DAY = 0
NOTIFICATION_INTERVAL = 7

class TriggerEmployeeI9Expiration(TriggerI9ExpirationBase):
    def __init__(self):
        super(TriggerEmployeeI9Expiration, self).__init__()

    def _check_schedule(self, expiration_date):
        if (not expiration_date):
            return False

        # Document creation should always be earlier than or the same as today
        date_diff = (date.today() - expiration_date.date()).days

        # Current schedule settings:
        #  - between 7 days before and 0 days before expiration date, send daily
        #  - prior to 28 days before expiration date, send one every 7 days
        #  - after expiration, stop notification
        if ((date_diff <= NOTIFICATION_INTERVAL and date_diff >= TERMINATE_NOTIFICATiON_DAY)
            or (date_diff <= EMAIL_START_DAY and date_diff % NOTIFICATION_INTERVAL == 0)):
            return True
        return False
