import reversion

from django.db import models
from company_std_insurance_plan import CompanyStdInsurancePlan

@reversion.register
class CompanyStdAgeBasedRate(models.Model):
    company_std_insurance_plan = models.ForeignKey(CompanyStdInsurancePlan,
                                                   related_name="age_based_rates")
    age_min = models.SmallIntegerField(blank=True,
                                       null=True,
                                       verbose_name="Min value of age.")

    age_max = models.SmallIntegerField(blank=True,
                                       null=True,
                                       verbose_name="Max value of age.")

    rate = models.DecimalField(max_digits=20,
                               decimal_places=10,
                               blank=False,
                               null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
