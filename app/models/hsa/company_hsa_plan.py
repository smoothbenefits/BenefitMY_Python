import reversion

from django.db import models
from app.models.company import Company

@reversion.register
class CompanyHsaPlan(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name="company_hsa_plan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
