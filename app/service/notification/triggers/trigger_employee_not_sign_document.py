from datetime import date
from trigger_not_sign_document_base import TriggerNotSignDocumentBase


class TriggerEmployeeNotSignDocument(TriggerNotSignDocumentBase):
    def __init__(self):
        super(TriggerEmployeeNotSignDocument, self).__init__()

    def _check_schedule(self, created_date):
        if (not created_date):
            return False

        # Document creation should always be earlier than or the same as today
        date_diff = (date.today() - created_date).days

        # Current schedule settings:
        #  - between 26 days after and 35 days after created date, send daily
        #  - prior to 26 days after created date, send one every 5 days
        #  - post 35 days after created date, stop notification
        if ((date_diff >= 26 and date_diff <= 35)
            or (date_diff < 26 and date_diff % 5 == 0)):
            return True
        return False
