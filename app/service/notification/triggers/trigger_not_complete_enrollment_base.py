from datetime import date

from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from app.models.person import (Person, SELF)
from app.models.employee_profile import (
    EmployeeProfile,
    EMPLYMENT_STATUS_TERMINATED)
from app.service.user_enrollment_summary_service import(
    UserEnrollmentSummaryService,
    COMPLETED,
    NO_BENEFITS)
from trigger_base import TriggerBase


class TriggerNotCompleteEnrollmentBase(TriggerBase):
    def __init__(self):
        super(TriggerNotCompleteEnrollmentBase, self).__init__()

    def _examine_condition(self):
        self._refresh_cached_data()

        company_users = CompanyUser.objects.filter(company_user_type=USER_TYPE_EMPLOYEE)

        for company_user in company_users:
            user = company_user.user
            company = company_user.company
            person = None
            employee_profile = None
            persons = Person.objects.filter(user=user.id, relationship=SELF)
            if (len(persons) > 0):
                person = persons[0]
                employee_profiles = person.employee_profile_person.all()
                if (len(employee_profiles) > 0):
                    employee_profile = employee_profiles[0]

            if (not user
                or not company
                or not person
                or not employee_profile
                or employee_profile.employment_status == EMPLYMENT_STATUS_TERMINATED):
                # skip if user does not have sufficient information to trigger
                # the action
                continue

            start_date = employee_profile.start_date

            # skip if this user's start date does not meet notification
            # schedule
            if (not self._check_schedule(start_date)):
                continue

            # Now check for whether the user has completed enrollment
            enroll_service = UserEnrollmentSummaryService(company.id, user.id, person.id) 
            if (not enroll_service.get_enrollment_status() == COMPLETED):
                self._cache_company_user(company.id, user.id)

        return (not self._is_cached_data_empty())

    def _refresh_cached_data(self):
        raise NotImplementedError

    def _cache_company_user(self, company_id, user_id):
        raise NotImplementedError

    def _is_cached_data_empty(self):
        raise NotImplementedError

    def _check_schedule(self, start_date):
        raise NotImplementedError

    def _get_action_data(self):
        raise NotImplementedError
