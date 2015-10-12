import reversion

from django.db import models

from company_extra_benefit_plan import CompanyExtraBenefitPlan


@reversion.register
class ExtraBenefitItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)

    company_plan = models.ForeignKey(
        CompanyExtraBenefitPlan,
        related_name="benefit_items",
        blank=True,
        null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
