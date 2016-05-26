from datetime import date
from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from app.models.employment_authorization import EmploymentAuthorization
from trigger_company_user_base import TriggerCompanyUserBase


EMAIL_START_DAY = 28
TERMINATE_NOTIFICATION_DAY = 0
NOTIFICATION_INTERVAL = 7

class TriggerEmployeeI9Expiration(TriggerCompanyUserBase):
    def __init__(self):
        super(TriggerEmployeeI9Expiration, self).__init__()

    def _examine_condition(self):
        super(TriggerEmployeeI9Expiration, self)._refresh_cache()
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

    def _check_schedule(self, expiration_date):
        if (not expiration_date):
            return False

        # I9 Expiration creation should always be later than or the same as today
        date_diff = (expiration_date - date.today()).days

        # Current schedule settings:
        #  - between 7 days before and 0 days before expiration date, send daily
        #  - prior to 28 days before expiration date, send one every 7 days
        #  - after expiration, stop notification
        if ((date_diff <= NOTIFICATION_INTERVAL and date_diff >= TERMINATE_NOTIFICATION_DAY)
            or (date_diff <= EMAIL_START_DAY and date_diff % NOTIFICATION_INTERVAL == 0)):
            return True
        return False
