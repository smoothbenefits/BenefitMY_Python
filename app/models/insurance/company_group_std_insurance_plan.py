import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan


@reversion.register
class CompanyGroupStdInsurancePlan(models.Model):

    company_group = models.ForeignKey(CompanyGroup,
        related_name="company_std_insurance_plan")

    company_std_insurance_plan = models.ForeignKey(CompanyStdInsurancePlan,
                                            related_name="company_group_std")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)