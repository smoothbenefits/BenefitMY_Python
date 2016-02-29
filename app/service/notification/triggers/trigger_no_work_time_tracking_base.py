from datetime import date

from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from trigger_base import TriggerBase
from app.service.application_feature_service import ApplicationFeatureService
from app.service.time_tracking_service import TimeTrackingService
from app.service.date_time_service import DateTimeService


class TriggerNoWorkTimeTrackingBase(TriggerBase):
    def __init__(self):
        super(TriggerNoWorkTimeTrackingBase, self).__init__()

    def _examine_condition(self):
        self._refresh_cached_data()

        # Use the appropriate service to get the list of companies that
        # do not use this feature
        app_feature_service = ApplicationFeatureService()
        feature_disabled_company_list = app_feature_service.get_company_list_with_feature_disabled('WorkTimeSheet')

        # Get the start date of the past week (starting Sunday)
        week_start_date = self._get_last_week_start_date()

        # Get the list of users that have submitted the timesheet
        # for the week
        time_tracking_service = TimeTrackingService()
        submitted_users = time_tracking_service.get_all_users_submitted_work_timesheet_by_week_start_date(week_start_date)

        company_users = CompanyUser.objects.filter(company_user_type=USER_TYPE_EMPLOYEE)

        for company_user in company_users:
            user = company_user.user
            company = company_user.company

            # If the company does not use the feature, skip
            if (company.id in feature_disabled_company_list):
                continue

            # If the user has not submitted cache the information for action to follow
            if user.id not in submitted_users:
                # check schedule based on the oldest document
                if (self._check_schedule()):
                    self._cache_company_user(company.id, user.id)

        return (not self._is_cached_data_empty())

    def _get_last_week_start_date(self):
        date_time_service = DateTimeService()
        return date_time_service.get_last_week_range_by_date(date.today())[0]

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
