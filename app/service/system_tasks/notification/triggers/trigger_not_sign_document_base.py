from datetime import date

from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from app.models.document import Document
from trigger_company_user_base import TriggerCompanyUserBase


class TriggerNotSignDocumentBase(TriggerCompanyUserBase):
    def __init__(self):
        super(TriggerNotSignDocumentBase, self).__init__()

    def _examine_condition(self):
        super(TriggerNotSignDocumentBase, self)._examine_condition()

        company_users = CompanyUser.objects.filter(company_user_type=USER_TYPE_EMPLOYEE)

        for company_user in company_users:
            user = company_user.user
            company = company_user.company

            user_documents = Document.objects.filter(user=user.id)
            not_signed = [doc for doc in user_documents if not doc.signature]

            if len(not_signed) > 0:
                # sort unsigned document by creation date
                not_signed_sorted = sorted(not_signed, key=lambda doc: doc.created_at)
                # check schedule based on the oldest document
                if (self._check_schedule(not_signed_sorted[0].created_at)):
                    self._cache_company_user(company.id, user.id)

        return (not self._is_cached_data_empty())

    def _check_schedule(self, created_date):
        raise NotImplementedError()
