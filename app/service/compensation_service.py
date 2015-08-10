from app.models.employee_compensation import EmployeeCompensation
from django.utils import timezone

class CompensationService(object):
    def __init__(self, person_id):
        self.person_id = person_id

    def _get_compensation_records_order_by_effective_date(self):
        try:
            return EmployeeCompensation.objects.filter(person_id=self.person_id)
        except EmployeeCompensation.DoesNotExist:
            return None

    def get_current_annual_salary(self):
        comps = self._get_compensation_records_order_by_effective_date()
        if not comps:
            raise ValueError('No Salary Records')
        current_salary = None
        for comp in comps:
            if comp.effective_date < timezone.now():
                current_salary = comp.annual_base_salary
                break
        if not current_salary:
            raise ValueError('No Salary Records')
        return current_salary

