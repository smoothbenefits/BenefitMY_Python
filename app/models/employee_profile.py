import reversion

from django.db import models
from person import Person

EMPLOYMENT_TYPES = ([(item, item) for item in ['FullTime', 'PartTime', 'Contractor', 'Intern']])
EMPLOYMENT_STATUS = ([(item, item) for item in ['Active', 'Prospective', 'Terminated', 'OnLeave']])

@reversion.register
class EmployeeProfile(models.Model):
    job_title = models.CharField(max_length=50, null=True)
    annual_base_salary = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    employment_type = models.CharField(
        max_length=30, choices=EMPLOYMENT_TYPES, null=True, blank=True)
    employment_status = models.CharField(
        max_length=20, choices=EMPLOYMENT_STATUS, null=True, blank=True)

    person = models.ForeignKey(Person,
                                related_name="employee_profile_person",
                                null=True,
                                blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
