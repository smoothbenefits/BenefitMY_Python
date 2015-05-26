import reversion

from django.db import models
from ..company import Company
from hra_plan import HraPlan

@reversion.register
class CompanyHraPlan(models.Model):
    hra_plan = models.ForeignKey(
        HraPlan,
        related_name="company_hra_plan")
    
    company = models.ForeignKey(
        Company,
        related_name="company_hra_plan")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
