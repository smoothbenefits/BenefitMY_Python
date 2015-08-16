import datetime
import reversion

from django.db import models
from person import Person
from company import Company
from sys_period_definition import SysPeriodDefinition

EMPLOYMENT_TYPES = ([(item, item) for item in ['FullTime', 'PartTime', 'Contractor', 'Intern']])
EMPLOYMENT_STATUS = ([(item, item) for item in ['Active', 'Prospective', 'Terminated', 'OnLeave']])

@reversion.register
class EmployeeProfile(models.Model):
    job_title = models.CharField(max_length=50, blank=True, null=True)

    annual_base_salary = models.DecimalField(max_digits=12, decimal_places=2,
                                             blank=True, null=True)

    start_date = models.DateField(blank=True, null=True)

    end_date = models.DateField(blank=True, null=True)

    employment_type = models.CharField(max_length=30, choices=EMPLOYMENT_TYPES,
                                       null=True, blank=True)

    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS,
                                         null=True, blank=True)

    pay_rate = models.ForeignKey(SysPeriodDefinition,
                                 related_name="employee_profile_pay_rate",
                                 blank=True,
                                 null=True)

    person = models.ForeignKey(Person,
                               default=0,
                               related_name="employee_profile_person")

    company = models.ForeignKey(Company,
                                default=0,
                                related_name="employee_profile_company")

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)

    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    class Meta:
        unique_together = ('person', 'company')
