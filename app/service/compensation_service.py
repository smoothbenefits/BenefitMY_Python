from django.utils import timezone
from datetime import datetime, date
from app.models.employee_compensation import EmployeeCompensation
from app.models.employee_profile import EmployeeProfile, FULL_TIME
from app.dtos.compensation_info import CompensationInfo

DEFAULT_COMPENSATION_HOURS_IN_YEAR = 40 * 52

'''
This is the service to provide compensation information to who ever needs it.
The service only needs the person_id where compensation is needed
'''
class CompensationService(object):
    def __init__(self, person_id, profile=None):
        self.person_id = person_id
        self.profile = profile

    def _is_fulltime_employee(self):
        if not self.profile:
            profiles = EmployeeProfile.objects.filter(person_id=self.person_id)
            if profiles and len(profiles) > 0:
                self.profile = profiles[0]

        if self.profile:
            return self.profile.employment_type == FULL_TIME
        return False

    def _get_compensation_records_order_by_effective_date(self, ascending=True):
        order = 'effective_date'
        if not ascending:
            order = '-' + order
        try:
            return EmployeeCompensation.objects.filter(person_id=self.person_id).order_by(order)
        except EmployeeCompensation.DoesNotExist:
            return None

    def _calculate_annual_salary(self, compensation, is_fulltime=True):
        current_salary = None
        if is_fulltime and compensation.annual_base_salary:
            current_salary = compensation.annual_base_salary
            return current_salary

        if (compensation.hourly_rate and compensation.projected_hour_per_month):
            current_salary = compensation.hourly_rate * compensation.projected_hour_per_month * 12

        return current_salary

    def _get_current_compensation(self):
        current_comp = None
        comps = self.get_all_compensation_ordered()
        if not comps:
            return current_comp

        decending_comps = comps[::-1]
        for comp in decending_comps:
            current_comp = comp
            if current_comp.effective_date < timezone.now():
                break
        return current_comp

    def get_current_annual_salary(self):
        current_salary = 0
        comp = self._get_current_compensation()
        if not comp:
            return current_salary

        is_fulltime = self._is_fulltime_employee()
        return self._calculate_annual_salary(comp, is_fulltime)

    def get_current_weekly_salary(self, weekly_hours):
        weekly_salary = 0
        comp = self._get_current_compensation()
        if not comp:
            return weekly_salary

        days_in_year = date(datetime.now().year, 12, 31).timetuple().tm_yday
        is_fulltime = self._is_fulltime_employee()
        if is_fulltime and comp.annual_base_salary:
            return comp.annual_base_salary / days_in_year * 7
        elif comp.hourly_rate:
            return comp.hourly_rate * weekly_hours

    def get_current_hourly_rate(self):
        hourly_rate = None

        comp = self._get_current_compensation()
        if not comp:
            return hourly_rate

        is_fulltime = self._is_fulltime_employee()

        if is_fulltime and comp.annual_base_salary:
            hourly_rate = comp.annual_base_salary / DEFAULT_COMPENSATION_HOURS_IN_YEAR
        elif (comp.hourly_rate):
            hourly_rate = comp.hourly_rate

        return hourly_rate

    def get_all_compensation_ordered(self):
        comps = self._get_compensation_records_order_by_effective_date()
        info_list = []
        for comp in comps:
            comp_info = CompensationInfo()
            comp_info.build_from_record(comp)
            info_list.append(comp_info)

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
                continue
            elif comp_info.annual_base_salary and not comp_info.hourly_rate:
                # We are in the full time employee case
                if base and base.annual_base_salary:
                    comp_info.increase_percentage = (comp_info.annual_base_salary - base.annual_base_salary) /base.annual_base_salary * 100
            elif comp_info.hourly_rate and not comp_info.annual_base_salary:
                # we are in the part time employee case
                if base and base.hourly_rate:
                    comp_info.increase_percentage = (comp_info.hourly_rate - base.hourly_rate) / base.hourly_rate * 100
            elif comp_info.increase_percentage:
                # Calculate the actual number based on increase percentage
                if base and base.hourly_rate:
                    comp_info.hourly_rate = base.hourly_rate + (base.hourly_rate * comp_info.increase_percentage / 100)
                elif base and base.annual_base_salary:
                    comp_info.annual_base_salary = base.annual_base_salary + (base.annual_base_salary * comp_info.increase_percentage / 100)
            else:
                raise ValueError('Compensation record with both annual_base_salary and hourly_rate defined. This is invalid record')
            base = comp_info
        return info_list
