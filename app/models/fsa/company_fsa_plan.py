import reversion

from django.db import models
from fsa import FSA
from app.models.company import Company

@reversion.register
class CompanyFsaPlan(models.Model):
    company = models.ForeignKey(Company,
                                blank=True,
                                null=True)
    fsa_plan = models.ForeignKey(FSA,
                                 blank=True,
                                 null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
