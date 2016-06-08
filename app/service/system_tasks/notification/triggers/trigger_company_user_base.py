from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from ...trigger_base import TriggerBase


class TriggerCompanyUserBase(TriggerBase):
    def __init__(self):
        super(TriggerCompanyUserBase, self).__init__()
        self._company_user_cache = dict()

    def _examine_condition(self):
        self._refresh_cache()
        
        
    def _cache_company_user(self, company_id, user_id):
        if (company_id not in self._company_user_cache):
            self._company_user_cache[company_id] = []
        self._company_user_cache[company_id].append(user_id)

    def _refresh_cache(self):
        self._company_user_cache = dict()

    def _is_cached_data_empty(self):
        return len(self._company_user_cache) <= 0

    def _get_action_data(self):
        return {
            'company_user_id_list': self._company_user_cache
        }

    def _check_schedule(self, expiration_date):
        raise NotImplementedError()
