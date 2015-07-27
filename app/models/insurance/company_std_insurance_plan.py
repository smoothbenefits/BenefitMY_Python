import reversion

from django.db import models
from ..company import Company
from std_insurance_plan import StdInsurancePlan

PAID_BY_PARTIES = ([(item, item) for item in ['Employee', 'Employer']])

@reversion.register
class CompanyStdInsurancePlan(models.Model):

    elimination_period_in_days = models.IntegerField(blank=True, null=True)

    # This is in Weeks for STD
    duration= models.IntegerField(blank=True, null=True)

    percentage_of_salary = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    max_benefit_weekly = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)

    rate = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)

    employer_contribution_percentage = models.DecimalField(max_digits=5,
                                                           decimal_places=2,
                                                           blank=True,
                                                           null=True)

    paid_by = models.CharField(max_length=20,
                              choices=PAID_BY_PARTIES,
                              null=True,
                              blank=True)

    company = models.ForeignKey(Company,
                                related_name="company_std_insurance",
                                blank=True,
                                null=True)
    std_insurance_plan = models.ForeignKey(StdInsurancePlan,
                                           related_name="company_std_insurance",
                                           blank=True,
                                           null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
