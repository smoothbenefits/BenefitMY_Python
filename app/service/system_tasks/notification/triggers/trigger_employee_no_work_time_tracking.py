from datetime import date, datetime
from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from trigger_company_user_base import TriggerCompanyUserBase
from app.service.application_feature_service import (
    ApplicationFeatureService,
    APP_FEATURE_WORKTIMESHEET,
    APP_FEATURE_WORKTIMESHEETNOTIFICATION,
    APP_FEATURE_RANGEDTIMECARD
)
from app.service.time_tracking_service import TimeTrackingService
from app.service.date_time_service import DateTimeService
from app.service.send_email_service import (
    SendEmailService,
    EMAIL_BLOCK_FEATURE_WORKTIMESHEETNOTIFICATION
)


# Weekday 6 is Sunday
NOTIFICATION_WEEKDAY = 6


class TriggerEmployeeNoWorkTimeTracking(TriggerCompanyUserBase):
    def __init__(self):
        super(TriggerEmployeeNoWorkTimeTracking, self).__init__()

    def _examine_condition(self):
        super(TriggerEmployeeNoWorkTimeTracking, self)._examine_condition()

        # Only proceed if schedule met
        if (self._check_schedule()):

            send_email_service = SendEmailService()

            # Use the appropriate service to get the list of companies that
            # do not use this feature
            app_feature_service = ApplicationFeatureService()
            timesheet_disabled_company_list = app_feature_service.get_company_list_with_feature_disabled(APP_FEATURE_WORKTIMESHEET)
            ranged_timecard_enabled_company_list = app_feature_service.get_company_list_with_feature_enabled(APP_FEATURE_RANGEDTIMECARD)
            feature_disabled_company_list = [c for c in timesheet_disabled_company_list if c not in ranged_timecard_enabled_company_list]

            timesheet_notify_enabled_company_list = app_feature_service.get_company_list_with_feature_enabled(APP_FEATURE_WORKTIMESHEETNOTIFICATION)

            # Get the start date of the past week (starting Sunday)
            week_start_date = self._get_last_week_start_date()

            # Get the list of users that have submitted the timesheet
            # for the week
            time_tracking_service = TimeTrackingService()
            submitted_users = time_tracking_service.get_all_users_submitted_work_timesheet_by_week_start_date(week_start_date)

            # Get the list of users that have the notification of this feature blocked
            blocked_users = send_email_service.get_all_users_blocked_for_email_feature(
                    EMAIL_BLOCK_FEATURE_WORKTIMESHEETNOTIFICATION
                )

            # Only include the employee for reporting if all of the below hold
            #   - Company has the feature on
            #   - Company has the notification feature on
            #   - User is not blocked for this notification 
            #   - User has not submitted yet
            company_users = CompanyUser.objects.filter(
                    company_user_type=USER_TYPE_EMPLOYEE,
                    company__in=timesheet_notify_enabled_company_list,
                ).exclude(
                    company__in=feature_disabled_company_list
                ).exclude(
                    user__in=blocked_users
                ).exclude(
                    user__in=submitted_users
                )

            for company_user in company_users:
                user = company_user.user
                company = company_user.company

                self._cache_company_user(company.id, user.id)

        return (not self._is_cached_data_empty())

    def _get_last_week_start_date(self):
        date_time_service = DateTimeService()
        return date_time_service.get_last_week_range_by_date(date.today())[0]

    def _check_schedule(self):
        weekday = datetime.now().weekday()
        return weekday == NOTIFICATION_WEEKDAY
