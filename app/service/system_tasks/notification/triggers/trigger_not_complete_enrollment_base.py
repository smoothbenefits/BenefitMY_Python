from datetime import date

from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from app.models.person import (Person, SELF)
from app.models.employee_profile import (
    EmployeeProfile,
    EMPLOYMENT_STATUS_TERMINATED)
from app.service.user_enrollment_summary_service import(
    UserEnrollmentSummaryService,
    COMPLETED,
    NO_BENEFITS)
from trigger_company_user_base import TriggerCompanyUserBase


class TriggerNotCompleteEnrollmentBase(TriggerCompanyUserBase):
    def __init__(self):
        super(TriggerNotCompleteEnrollmentBase, self).__init__()

    def _examine_condition(self):
        super(TriggerNotCompleteEnrollmentBase, self)._examine_condition()

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

            # skip if user does not have sufficient information to trigger
            # the action
            if (not user
                or not company
                or not person
                or not employee_profile):
                continue

            # skip if the user
            #   - is not an active employee
            #   - or is not a new employee
            if (employee_profile.employment_status == EMPLOYMENT_STATUS_TERMINATED
                or not company_user.new_employee):
                continue

            # Take the benefit start date as the checkout point
            # Only as a safety net, if benefit start date is not available
            # for any reason, take the employee start date
            start_date = employee_profile.benefit_start_date
            if (not start_date):
                start_date = employee_profile.start_date

            # skip if this user's start date does not meet notification
            # schedule
            if (not self._check_schedule(start_date)):
                continue

            # Now check for whether the user has completed enrollment
            enroll_service = UserEnrollmentSummaryService(company.id, user.id, person.id) 
            if (enroll_service.get_enrollment_status() not in [NO_BENEFITS, COMPLETED]):
                self._cache_company_user(company.id, user.id)

        return (not self._is_cached_data_empty())

    def _check_schedule(self, start_date):
        raise NotImplementedError
