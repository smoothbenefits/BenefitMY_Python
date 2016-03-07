from datetime import date
from trigger_not_sign_document_base import TriggerNotSignDocumentBase

DAILY_EMAIL_START_DAY = 26
TERMINATE_NOTIFICATiON_DAY = 35
NOTIFICATION_INTERVAL = 5

class TriggerEmployeeNotSignDocument(TriggerNotSignDocumentBase):
    def __init__(self):
        super(TriggerEmployeeNotSignDocument, self).__init__()

    def _check_schedule(self, created_date):
        if (not created_date):
            return False

        # Document creation should always be earlier than or the same as today
        date_diff = (date.today() - created_date.date()).days

        # Current schedule settings:
        #  - between 26 days after and 35 days after created date, send daily
        #  - prior to 26 days after created date, send one every 5 days
        #  - post 35 days after created date, stop notification
        if ((date_diff >= DAILY_EMAIL_START_DAY and date_diff <= TERMINATE_NOTIFICATiON_DAY)
            or (date_diff < DAILY_EMAIL_START_DAY and date_diff % NOTIFICATION_INTERVAL == 0)):
            return True
        return False
