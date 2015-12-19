import reversion

from django.db import models
from company_hsa_plan import CompanyHsaPlan
from app.models.company_group import CompanyGroup

@reversion.register
class CompanyGroupHsaPlan(models.Model):
    company_group = models.ForeignKey(CompanyGroup, related_name="company_group_hsa_plan")
    company_hsa_plan = models.ForeignKey(CompanyHsaPlan, related_name="company_group_hsa_plan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
