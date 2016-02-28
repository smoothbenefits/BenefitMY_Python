from datetime import date

from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from trigger_base import TriggerBase
from app.service.application_feature_service import ApplicationFeatureService


class TriggerNoWorkTimeTrackingBase(TriggerBase):
    def __init__(self):
        super(TriggerNoWorkTimeTrackingBase, self).__init__()

    def _examine_condition(self):
        self._refresh_cached_data()

        # Use the appropriate service to get the list of companies that
        # do not use this feature
        app_feature_service = ApplicationFeatureService()
        company_list = app_feature_service.get_company_list_with_feature_disabled('WorkTimeSheet')

        company_users = CompanyUser.objects.filter(company_user_type=USER_TYPE_EMPLOYEE)

        for company_user in company_users:
            user = company_user.user
            company = company_user.company

            # If the company does not use the feature, skip
            if (company.id in company_list):
                continue

            # Check whether condition is met
            # TODO: 
            # - First Check whether the feature is enabled
            # - Then Get all time sheets from last week
            #   Build [company, [user, boolean]] dict
            #   For each company user, check whether exists
            #   If not, cache the company user. 
            #   This would need to handle env-aware hashed IDs
            condition_met = True

            if condition_met:
                # check schedule based on the oldest document
                if (self._check_schedule()):
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

    def _check_schedule(self):
        raise NotImplementedError()
