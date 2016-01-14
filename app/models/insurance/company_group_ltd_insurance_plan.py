import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.insurance.company_ltd_insurance_plan import \
    CompanyLtdInsurancePlan


@reversion.register
class CompanyGroupLtdInsurancePlan(models.Model):

    company_group = models.ForeignKey(CompanyGroup,
        related_name="company_ltd_insurance_plan")

    company_ltd_insurance_plan = models.ForeignKey(CompanyLtdInsurancePlan,
                                            related_name="company_group_ltd")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
