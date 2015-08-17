from django.utils import timezone
from app.models.employee_compensation import EmployeeCompensation
from app.models.employee_profile import EmployeeProfile

class CompensationService(object):
    def __init__(self, person_id):
        self.person_id = person_id

    def _is_fulltime_employee(self):
        profile = EmployeeProfile.objects.get(person_id=self.person_id)
        return profile['employment_type'] == 'FullTime'

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
        is_fulltime = _is_fulltime_employee()
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
