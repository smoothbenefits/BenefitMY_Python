import reversion

from django.db import models
from ..company import Company
from ltd_insurance_plan import LtdInsurancePlan


@reversion.register
class CompanyLtdInsurancePlan(models.Model):

    elimination_period= models.IntegerField(blank=True, null=True)
    duration= models.IntegerField(blank=True, null=True)
    percentage_of_salary = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    max_benefit = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)

    company = models.ForeignKey(Company,
                                related_name="company_ltd_insurance",
                                blank=True,
                                null=True)
    ltd_insurance_plan = models.ForeignKey(LtdInsurancePlan,
                                           related_name="company_ltd_insurance",
                                           blank=True,
                                           null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
