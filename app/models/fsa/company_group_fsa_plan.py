import reversion

from django.db import models
from app.models.company_group import CompanyGroup
from app.models.fsa.company_fsa_plan import CompanyFsaPlan

@reversion.register
class CompanyGroupFsaPlan(models.Model):

    company_group = models.ForeignKey(CompanyGroup, related_name="fsa_plan")

    company_fsa_plan = models.ForeignKey(CompanyFsaPlan,
                                         related_name="company_group_fsa")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
