import reversion

from django.db import models
from fsa_plan import FsaPlan
from app.models.company import Company

@reversion.register
class CompanyFsaPlan(models.Model):
    company = models.ForeignKey(Company)
    fsa_plan = models.ForeignKey(FsaPlan)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
