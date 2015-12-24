import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan


@reversion.register
class CompanyGroupBasicLifeInsurancePlan(models.Model):

    company_group = models.ForeignKey(CompanyGroup,
        related_name="basic_life_insurance_plan")

    company_basic_life_insurance_plan = models.ForeignKey(CompanyLifeInsurancePlan,
                                            related_name="company_group_basic_life_insurance")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
