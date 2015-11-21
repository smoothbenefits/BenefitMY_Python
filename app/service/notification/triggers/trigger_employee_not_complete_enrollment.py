from datetime import date

from trigger_not_complete_enrollment_base import TriggerNotCompleteEnrollmentBase


class TriggerEmployeeNotCompleteEnrollment(TriggerNotCompleteEnrollmentBase):
    def __init__(self):
        super(TriggerEmployeeNotCompleteEnrollment, self).__init__()

    def _refresh_cached_data(self):
        self._cached_user_list = []

    def _cache_company_user(self, company_id, user_id):
        self._cached_user_list.append(user_id)

    def _is_cached_data_empty(self):
        return len(self._cached_user_list) <= 0

    def _check_schedule(self, benefit_start_date):
        if (not benefit_start_date):
            return False

        date_diff = (benefit_start_date - date.today()).days

        # Current schedule settings:
        #  - between 4 days before and 4 days after start date, send daily
        #  - prior to 4 days before start date, send one every 5 days
        #  - post 4 days after start date, stop notification
        if ((date_diff >= -4 and date_diff <= 4)
            or (date_diff > 4 and date_diff % 5 == 0)):
            return True
        return False

    def _get_action_data(self):
        return {
            'user_id_list': self._cached_user_list
        }
