from django.utils import timezone
import datetime
from app.models.company_user import (
    CompanyUser,
    USER_TYPE_EMPLOYEE
)
from app.models.employee_profile import (
    EmployeeProfile,
    EMPLOYMENT_STATUS_ACTIVE,
    EMPLOYMENT_STATUS_PROSPECTIVE,
    EMPLOYMENT_STATUS_TERMINATED,
    EMPLOYMENT_STATUS_ONLEAVE
)
from app.service.date_time_service import DateTimeService


'''
This is the service to provide utility access to company personnels
knowledge
'''
class CompanyPersonnelService(object):

    def __init__(self):
        self._date_time_service = DateTimeService()

    def get_company_id_by_employee_user_id(self, employee_user_id):
        employees = CompanyUser.objects.filter(
            user=employee_user_id,
            company_user_type=USER_TYPE_EMPLOYEE)
        if (len(employees) > 0):
            return employees[0].company_id
        return None

    ''' Get all employees who is not fully terminated during the given
        time range. i.e. the employee has other employment statuses in
        the time range than 'Terminated'.
        This is to serve a common use case of where reports want to
        include only those employees that are at least partially relate
        to the company in the view port time range.
    '''
    def get_company_employee_user_ids_non_fully_terminated_in_time_range(
        self,
        company_id,
        time_range_start,
        time_range_end):
        all_employee_mappings = self._get_company_employee_user_ids_to_employment_statuses_map(
            company_id, time_range_start, time_range_end)
        filtered_user_ids = []

        for user_id in all_employee_mappings:
            for status in all_employee_mappings[user_id]:
                if (not status == EMPLOYMENT_STATUS_TERMINATED):
                    filtered_user_ids.append(user_id)
                    break

        return filtered_user_ids

    ''' Get all employees who are part of the specified employment status as of now
        This is to serve a common use case of where we want to know which
        employees are of the specified employment status
    '''
    def get_company_employee_user_ids_currently_with_status(self, company_id, employment_status):
        all_employee_mappings = self._get_company_employee_user_ids_to_employment_statuses_map(
            company_id,
            datetime.date.today(),
            datetime.date.today())
        
        employees_with_status = []
        for user_id in all_employee_mappings:
            for status in all_employee_mappings[user_id]:
                if employment_status == status:
                    employees_with_status.append(user_id)
                    break

        return employees_with_status

    ''' Get a mapping, where each pair represents a employee 
        mapped to a list that contains all employement statuses
        that were at least partially "on" during the given time
        range. 
        E.g. if an employee was working for the first 2 days in
        the time range, but got employment terminated since day 3,
        then this employee would map to a list that contains 2
        statuses: Active and Terminated.
    '''
    def _get_company_employee_user_ids_to_employment_statuses_map(
        self,
        company_id,
        time_range_start,
        time_range_end):
        result = {}
        all_employees = CompanyUser.objects.filter(
            company=company_id,
            company_user_type=USER_TYPE_EMPLOYEE)
        for employee in all_employees:
            # populate with empty values
            result[employee.user_id] = []

        all_employee_profiles = EmployeeProfile.objects.filter(
            company=company_id) 
        for employee_profile in all_employee_profiles:
            employee_user_id = employee_profile.person.user.id
            if (employee_user_id in result):
                result[employee_user_id] = self._get_employment_statuses_in_time_range(
                        employee_profile,
                        time_range_start,
                        time_range_end
                    )
            else:
                raise Exception('Found company employee profile for user that does not relate to the company! Offending user_id is: {}'.format(employee_user_id))

        return result

    def _get_employment_statuses_in_time_range(self, employee_profile, time_range_start, time_range_end):
        result = []

        # [TODO]: We currently don't model a complete trail of
        #       employment status changes, and hence we are 
        #       currently only able to infer some information
        #       from employee's start and end employment dates

        # Conditions
        #  * If employment start date after time range, result => [Prospective]
        #  * If employment end date prior to time range, result => [Terminated]
        #  * If employment start date prior to time range and end date after => [Active]
        #  * If employment start date within time range, result to include/add [Prospective, Active]
        #  * If employment end date within time range, result to include/add [Active, Terminated] 
        if ((employee_profile.start_date or datetime.date.min) > time_range_end):
            result = [EMPLOYMENT_STATUS_PROSPECTIVE]
        elif (employee_profile.end_date and employee_profile.end_date < time_range_start):
            result = [EMPLOYMENT_STATUS_TERMINATED]
        elif ((employee_profile.start_date or datetime.date.min) <= time_range_start
            and (not employee_profile.end_date or employee_profile.end_date >= time_range_end)):
            result = [EMPLOYMENT_STATUS_ACTIVE]

        if (self._date_time_service.is_time_in_range(
            employee_profile.start_date or datetime.date.min, time_range_start, time_range_end)):
            self._ensure_value_in_list(result, EMPLOYMENT_STATUS_PROSPECTIVE)
            self._ensure_value_in_list(result, EMPLOYMENT_STATUS_ACTIVE)

        if (employee_profile.end_date and self._date_time_service.is_time_in_range(
            employee_profile.end_date, time_range_start, time_range_end)):
            self._ensure_value_in_list(result, EMPLOYMENT_STATUS_ACTIVE)
            self._ensure_value_in_list(result, EMPLOYMENT_STATUS_TERMINATED)

        return result;

    def _ensure_value_in_list(self, input_list, value):
        if (not value):
            return
        if (value in input_list):
            return 

        input_list.append(value)
