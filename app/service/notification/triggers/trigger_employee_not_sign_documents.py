from datetime import date

from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from app.models.document import Document
from trigger_base import TriggerBase


class TriggerNotSignDocumentsBase(TriggerBase):
    def __init__(self):
        super(TriggerNotSignDocumentsBase, self).__init__()

    def _examine_condition(self):
        self._refresh_cached_data()

        company_users = CompanyUser.objects.filter(company_user_type=USER_TYPE_EMPLOYEE)

        for company_user in company_users:
            user = company_user.user
            company = company_user.company
            user_documents = Document.objects.filter(user=user.id)
            not_signed = [doc for doc in user_documents if not doc.signature]
            if len(not_signed) > 0:
                self._cache_company_user(company.id, user.id)

        return (not self._is_cached_data_empty())

    def _refresh_cached_data(self):
        self._cached_company_user_list = dict()

    def _cache_company_user(self, company_id, user_id):
        if (company_id not in self._cached_company_user_list):
            self._cached_company_user_list[company_id] = []
        self._cached_company_user_list[company_id].append(user_id)

    def _is_cached_data_empty(self):
        return len(self._cached_company_user_list) <= 0

    def _get_action_data(self):
        return {
            'company_user_id_list': self._cached_company_user_list
        }

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
