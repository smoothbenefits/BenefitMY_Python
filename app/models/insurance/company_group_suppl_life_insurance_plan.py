import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.insurance.comp_suppl_life_insurance_plan import \
    CompSupplLifeInsurancePlan


@reversion.register
class CompanyGroupSupplLifeInsurancePlan(models.Model):

    company_group = models.ForeignKey(CompanyGroup,
        related_name="suppl_life_insurance_plan")

    company_suppl_life_insurance_plan = models.ForeignKey(CompSupplLifeInsurancePlan,
                                            related_name="company_group_suppl_life_insurance")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
