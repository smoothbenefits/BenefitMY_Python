from datetime import date
from trigger_not_sign_document_base import TriggerNotSignDocumentBase


class TriggerCompanyNotSignDocument(TriggerNotSignDocumentBase):
    def __init__(self):
        super(TriggerCompanyNotSignDocument, self).__init__()

    def _check_schedule(self, created_date):
        if (not created_date):
            return False

        # Document creation should always be earlier than or the same as today
        date_diff = (date.today() - created_date).days

        # Current schedule settings:
        #  - 35 days after created date, send notification to employer
        if (date_diff == 35):
            return True

        return False
