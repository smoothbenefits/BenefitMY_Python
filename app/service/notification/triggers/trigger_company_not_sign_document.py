from datetime import date
from trigger_not_sign_document_base import TriggerNotSignDocumentBase

TERMINATE_NOTIFICATiON_DAY = 35

class TriggerCompanyNotSignDocument(TriggerNotSignDocumentBase):
    def __init__(self):
        super(TriggerCompanyNotSignDocument, self).__init__()

    def _check_schedule(self, created_date):
        if (not created_date):
            return False

        # Document creation should always be earlier than or the same as today
        date_diff = (date.today() - created_date.date()).days

        # Current schedule settings:
        #  - 35 days after created date, send notification to employer
        if (date_diff == TERMINATE_NOTIFICATiON_DAY):
            return True

        return False
