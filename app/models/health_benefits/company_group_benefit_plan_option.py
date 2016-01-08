import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.health_benefits.company_benefit_plan_option import \
    CompanyBenefitPlanOption


@reversion.register
class CompanyGroupBenefitPlanOption(models.Model):

    company_group = models.ForeignKey(CompanyGroup,
        related_name="health_benefit_plan_option")

    company_benefit_plan_option = models.ForeignKey(CompanyBenefitPlanOption,
                                            related_name="company_group_benefit_plan_option")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
