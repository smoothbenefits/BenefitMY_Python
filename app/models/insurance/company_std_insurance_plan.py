import reversion

from django.db import models
from ..company import Company
from std_insurance_plan import StdInsurancePlan


@reversion.register
class CompanyStdInsurancePlan(models.Model):

    percentage_of_salary = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    max_benefit = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)

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
