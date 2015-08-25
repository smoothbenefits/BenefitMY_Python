from django.utils import timezone
from app.models.employee_compensation import EmployeeCompensation
from app.models.employee_profile import EmployeeProfile, FULL_TIME
from app.view_models.compensation_info import CompensationInfo

'''
This is the service to provide compensation information to who ever needs it.
The service only needs the person_id where compensation is needed
'''
class CompensationService(object):
    def __init__(self, person_id):
        self.person_id = person_id

    def _is_fulltime_employee(self):
        profiles = EmployeeProfile.objects.filter(person_id=self.person_id)
        if profiles and len(profiles) > 0:
            return profiles[0].employment_type == FULL_TIME

    def _get_compensation_records_order_by_effective_date(self, ascending=True):
        order = 'effective_date'
        if not ascending:
            order = '-' + order
        try:
            return EmployeeCompensation.objects.filter(person_id=self.person_id).order_by(order)
        except EmployeeCompensation.DoesNotExist:
            return None

    def get_current_annual_salary(self):
        comps = self._get_compensation_records_order_by_effective_date(False)
        if not comps:
            raise ValueError('No Salary Records')
        current_salary = None
        is_fulltime = self._is_fulltime_employee()
        for comp in comps:
            if comp.effective_date < timezone.now():
                if is_fulltime:
                    current_salary = comp.annual_base_salary
                else:
                    # for part time employee, get projected annual wage
                    current_salary = comp.hourly_rate * comp.projected_hour_per_month * 12
                break
        if not current_salary:
            raise ValueError('No Salary Records')
        return current_salary

    def get_all_compensation_ordered(self):
        comps = self._get_compensation_records_order_by_effective_date()
        info_list = []
        for comp in comps:
            info_list.append(CompensationInfo(comp))

        base = None
        current = None
        for comp_info in info_list:
            # Mark which compensation can be marked as the current compensation in effect
            if comp_info.effective_date < timezone.now():
                if not current:
                    current = comp_info
                    current.is_current = True
                elif comp_info.effective_date >= current.effective_date:
                    comp_info.is_current = True
                    current.is_current = False
                    current = comp_info
            # Now calculate all the values of the compensation records
            if not comp_info.annual_base_salary and not comp_info.hourly_rate and not base:
                raise ValueError("The compensation list do not have a valid base record")
            elif comp_info.annual_base_salary and not comp_info.hourly_rate:
                # We are in the full time employee case
                if base:
                    comp_info.increase_percentage = (comp_info.annual_base_salary - base.annual_base_salary) /base.annual_base_salary * 100
            elif comp_info.hourly_rate and not comp_info.annual_base_salary:
                # we are in the part time employee case
                if base:
                    comp_info.increase_percentage = (comp_info.hourly_rate - base.hourly_rate) / base.hourly_rate * 100
            elif comp_info.increase_percentage:
                # Calculate the actual number based on increase percentage
                if base and base.hourly_rate:
                    comp_info.hourly_rate = base.hourly_rate + (base.hourly_rate * comp_info.increase_percentage / 100)
                elif base and base.annual_base_salary:
                    comp_info.annual_base_salary = base.annual_base_salary + (base.annual_base_salary * comp_info.increase_percentage / 100)
            base = comp_info
        return info_list

    def convert_to_json(self, comp_list):
        json_array = []
        if not comp_list:
            return json_array
        for comp_info in comp_list:
            json_array.append(comp_info.to_json())
        return json_array

