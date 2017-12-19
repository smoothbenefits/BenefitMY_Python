from datetime import date
from app.models.employee_profile import (
    EmployeeProfile,
    FULL_TIME
)
from app.models.company_user import (
    CompanyUser,
    USER_TYPE_EMPLOYEE
)

from app.service.compensation_service import (
    CompensationService,
    PAY_TYPE_HOURLY,
    PAY_TYPE_SALARY
)

class EmployeeEmploymentProfileInfo(object):

    def __init__(self, person_model, company_model, employee_user_id, profile_model=None):
        self._employee_profile_model = None
        self._compensation_service = None
        self._employee_user_id = employee_user_id
        self._company_model = company_model
        self._is_new_employee = None

        if (person_model):
            try:
                if (profile_model):
                    self._employee_profile_model = profile_model
                else:
                    self._employee_profile_model = EmployeeProfile.objects.get(
                                                company=company_model.id,
                                                person=person_model.id)
                self._compensation_service = CompensationService(
                    person_model=person_model,
                    profile=self._employee_profile_model)
            except EmployeeProfile.DoesNotExist:
                pass

        self.job_title = ''
        self.employee_number = ''
        self.hire_date = ''
        self.end_date =''
        self.pay_cycle = ''
        self.employment_status = ''
        self.projected_hours_per_pay_cycle = ''
        self.projected_hours_per_week = ''
        self.pay_type = ''
        self.compensation_effective_date = ''
        self.current_hourly_rate = ''
        self.current_pay_period_salary = ''
        self.annual_salary = ''
        self.employment_type = ''
        self.department = None
        self.division = None
        self.job = None

        if (self._employee_profile_model):
            self.job_title = self._employee_profile_model.job_title
            self.employee_number = self._employee_profile_model.employee_number
            self.hire_date = self._employee_profile_model.start_date
            self.end_date = self._employee_profile_model.end_date
            self.pay_cycle = company_model.pay_period_definition.name
            self.employment_status = self._employee_profile_model.employment_status
            self.employment_type = self._employee_profile_model.employment_type

            if (self._employee_profile_model.department):
                self.department = Department(
                    self._employee_profile_model.department.department,
                    self._employee_profile_model.department.code)

            if (self._employee_profile_model.division):
                self.division = Division(
                    self._employee_profile_model.division.division,
                    self._employee_profile_model.division.code)

            if (self._employee_profile_model.job):
                self.job = Job(
                    self._employee_profile_model.job.job,
                    self._employee_profile_model.job.code)

            if (self._compensation_service):
                current_compensation = self._compensation_service.current_compensation
                
                if (current_compensation):
                    projected_hours_cycle = self._get_projected_hours_per_pay_cycle(
                        current_compensation,
                        company_model.pay_period_definition
                    )
                    if (projected_hours_cycle):
                        self.projected_hours_per_pay_cycle = projected_hours_cycle

                    projected_hours_week = self._get_projected_hours_per_week(
                        current_compensation
                    )
                    if (projected_hours_week):
                        self.projected_hours_per_week = projected_hours_week

                    pay_type = self._compensation_service.get_current_pay_type()
                    if (pay_type):
                        self.pay_type = pay_type 

                    self.compensation_effective_date = current_compensation.effective_date

                    if (self.pay_type == PAY_TYPE_HOURLY):
                        self.current_hourly_rate = self._compensation_service.get_current_hourly_rate()
                    elif (self.pay_type == PAY_TYPE_SALARY):
                        self.annual_salary = self._compensation_service.get_current_annual_salary()
                        self.current_pay_period_salary = self._get_pay_period_salary(
                            self.annual_salary,
                            company_model.pay_period_definition
                        )

    @property
    def new_employee(self):
        if (self._is_new_employee is None):
            company_user = CompanyUser.objects.get(
                user=self._employee_user_id,
                company_user_type=USER_TYPE_EMPLOYEE,
                company=self._company_model.id)

            self._is_new_employee = company_user.new_employee
        return self._is_new_employee

    def _get_projected_hours_per_pay_cycle(self, compensation_info, pay_period_definition):
        if (compensation_info.projected_hour_per_month):
            return float(compensation_info.projected_hour_per_month) * pay_period_definition.month_factor
        return None

    def _get_projected_hours_per_week(self, compensation_info):
        if (compensation_info.projected_hour_per_month):
            return float(compensation_info.projected_hour_per_month) * 12 / 52
        return None

    def _get_pay_period_salary(self, annual_salary, pay_period_definition):
        if (not annual_salary):
            return annual_salary
        return float(annual_salary) / 12.0 * pay_period_definition.month_factor

    ''' Check if employee is active, at least partially, during the specified
        time period.
        The period_start and period_end are expected to be datetime objects
    '''
    def is_employee_active_anytime_in_time_period(self, period_start, period_end):
        # just return some dumb assumption for inputs not sufficient 
        # for determination
        if (not self.hire_date):
            return False

        # Compute the 2 date diffs to see if employee active period
        # overlaps the given time period to check
        # The 2 time range overlaps if the below 2 statements hold altogether
        #  * employee_start_date <= period_end
        #  * employee_end_date >= period_start
        return ((self.hire_date <= period_end)
            and (not self.end_date or self.end_date >= period_start))
    
    def is_full_time_employee(self):
        return self.employment_type == FULL_TIME


class Department(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code


class Job(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code


class Division(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code
