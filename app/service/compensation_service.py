from django.utils import timezone
from app.models.employee_compensation import EmployeeCompensation
from app.models.employee_profile import EmployeeProfile, FULL_TIME

class CompensationService(object):
    def __init__(self, person_id):
        self.person_id = person_id

    def _is_fulltime_employee(self):
        profiles = EmployeeProfile.objects.filter(person_id=self.person_id)
        if profiles and len(profiles) > 0:
            return profiles[0].employment_type == FULL_TIME

    def _get_compensation_records_order_by_effective_date(self):
        try:
            return EmployeeCompensation.objects.filter(person_id=self.person_id).order_by('-effective_date')
        except EmployeeCompensation.DoesNotExist:
            return None

    def get_current_annual_salary(self):
        comps = self._get_compensation_records_order_by_effective_date()
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
                    if (comp.hourly_rate and comp.projected_hour_per_month):
                        current_salary = comp.hourly_rate * comp.projected_hour_per_month * 12
                break
        if not current_salary:
            raise ValueError('No Salary Records')
        return current_salary
