from datetime import date

from trigger_not_complete_enrollment_base import TriggerNotCompleteEnrollmentBase


class TriggerCompanyNotCompleteEnrollment(TriggerNotCompleteEnrollmentBase):
    def __init__(self):
        super(TriggerCompanyNotCompleteEnrollment, self).__init__()

    def _refresh_cached_data(self):
        self._cached_company_user_list = dict()

    def _cache_company_user(self, company_id, user_id):
        if (company_id not in self._cached_company_user_list):
            self._cached_company_user_list[company_id] = []
        self._cached_company_user_list[company_id].append(user_id)

    def _is_cached_data_empty(self):
        return len(self._cached_company_user_list) <= 0

    def _check_schedule(self, benefit_start_date):
        if (not benefit_start_date):
            return False

        date_diff = (benefit_start_date - date.today()).days

        # Current schedule settings:
        #  - only check and trigger this on the 5th day after
        #    the benefit start date
        if (date_diff == -5):
            return True
        return False

    def _get_action_data(self):
        return {
            'company_user_id_list': self._cached_company_user_list
        }
