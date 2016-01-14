import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.commuter.company_commuter_plan import \
    CompanyCommuterPlan


@reversion.register
class CompanyGroupCommuterPlan(models.Model):

    company_group = models.ForeignKey(CompanyGroup,
        related_name="commuter_plan")

    company_commuter_plan = models.ForeignKey(CompanyCommuterPlan,
                                        related_name="company_group_commuter")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
