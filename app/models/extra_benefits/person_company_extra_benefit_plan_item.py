import reversion

from django.db import models
from person_company_extra_benefit_plan import PersonCompanyExtraBenefitPlan
from extra_benefit_item import ExtraBenefitItem


@reversion.register
class PersonCompanyExtraBenefitPlanItem(models.Model):

    person_company_extra_benefit_plan = models.ForeignKey(
        PersonCompanyExtraBenefitPlan,
        related_name="plan_items",
        blank=True,
        null=True)

    extra_benefit_item = models.ForeignKey(
        ExtraBenefitItem,
        related_name="person_company_extra_benefit_plans")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
