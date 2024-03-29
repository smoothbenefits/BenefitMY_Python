import datetime
import reversion

from django.db import models
from person import Person
from company import Company
from company_department import CompanyDepartment
from company_job import CompanyJob
from company_division import CompanyDivision
from sys_period_definition import SysPeriodDefinition

FULL_TIME = 'FullTime'
PART_TIME = 'PartTime'
CONTRACTOR = 'Contractor'
INTERN = 'Intern'
PER_DIEM = 'PerDiem'

EMPLOYMENT_TYPES = ([(item, item) for item in [FULL_TIME, PART_TIME, CONTRACTOR, INTERN, PER_DIEM]])

EMPLOYMENT_STATUS_ACTIVE = 'Active'
EMPLOYMENT_STATUS_PROSPECTIVE = 'Prospective'
EMPLOYMENT_STATUS_TERMINATED = 'Terminated'
EMPLOYMENT_STATUS_ONLEAVE = 'OnLeave'
EMPLOYMENT_STATUS = ([(item, item) for item in [EMPLOYMENT_STATUS_ACTIVE,EMPLOYMENT_STATUS_PROSPECTIVE,EMPLOYMENT_STATUS_TERMINATED,EMPLOYMENT_STATUS_ONLEAVE]])

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
                                         default=EMPLOYMENT_STATUS_ACTIVE)

    pay_rate = models.ForeignKey(SysPeriodDefinition,
                                 related_name="employee_profile_pay_rate",
                                 blank=True,
                                 null=True)

    benefit_start_date = models.DateField(blank=True, null=True)

    person = models.ForeignKey(Person,
                               default=0,
                               related_name="employee_profile_person")

    company = models.ForeignKey(Company,
                                default=0,
                                related_name="employee_profile_company")

    department = models.ForeignKey(CompanyDepartment,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="employee_profile_company_department")

    job = models.ForeignKey(CompanyJob,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="employee_profile_company_job")

    division = models.ForeignKey(CompanyDivision,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="employee_profile_company_division")

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)

    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    manager = models.ForeignKey('self',
                                related_name="direct_reports",
                                null=True,
                                blank=True)

    employee_number = models.TextField(blank=True, null=True)

    pin = models.TextField(blank=True, null=True)

    photo_url = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('person', 'company'), ('employee_number', 'company'), ('pin', 'company'))
