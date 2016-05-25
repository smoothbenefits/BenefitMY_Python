from app.models.employment_authorization import EmploymentAuthorization
from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from ...trigger_base import TriggerBase


class TriggerI9ExpirationBase(TriggerBase):
    def __init__(self):
        super(TriggerI9ExpirationBase, self).__init__()
        self._expiring_i9_company_user = dict()

    def _examine_condition(self):
        self._refresh_cache()
        expiring_i9_list = EmploymentAuthorization.objects.all().exclude(expiration_date__isnull=True)

        for expiring_i9 in expiring_i9_list:
            if self._check_schedule(expiring_i9.expiration_date):
                company_user = CompanyUser.objects.filter(
                    user=expiring_i9.user,
                    company_user_type=USER_TYPE_EMPLOYEE
                ).first()

                if company_user:
                    self._cache_company_user(company_user.company.id, company_user.user.id)

        return (not self._is_cached_data_empty())

    def _cache_company_user(self, company_id, user_id):
        if (company_id not in self._expiring_i9_company_user):
            self._expiring_i9_company_user[company_id] = []
        self._expiring_i9_company_user[company_id].append(user_id)

    def _refresh_cache(self):
        self._expiring_i9_company_user = dict()

    def _is_cached_data_empty(self):
        return len(self._expiring_i9_company_user) <= 0

    def _get_action_data(self):
        return {
            'company_user_id_list': self._expiring_i9_company_user
        }

    def _check_schedule(self, expiration_date):
        raise NotImplementedError()
