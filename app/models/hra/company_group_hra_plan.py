import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.hra.company_hra_plan import \
    CompanyHraPlan


@reversion.register
class CompanyGroupHraPlan(models.Model):

    company_group = models.ForeignKey(CompanyGroup,
        related_name="hra_plan")

    company_hra_plan = models.ForeignKey(CompanyHraPlan,
                                        related_name="company_group_hra")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
