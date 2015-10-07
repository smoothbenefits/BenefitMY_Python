import reversion

from django.db import models

from ..company import Company


@reversion.register
class CompanyExtraBenefitPlan(models.Model):
    description = models.CharField(max_length=4000, null=True, blank=True)

    company = models.ForeignKey(
        Company,
        related_name="company_extra_benefit_plan")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
