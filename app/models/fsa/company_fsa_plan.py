import reversion

from django.db import models
from fsa_plan import FsaPlan
from app.models.company import Company

@reversion.register
class CompanyFsaPlan(models.Model):
    company = models.ForeignKey(Company, related_name="company_fsa_plan_company")
    fsa_plan = models.ForeignKey(FsaPlan, related_name="company_fsa_plan_fsa_plan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
