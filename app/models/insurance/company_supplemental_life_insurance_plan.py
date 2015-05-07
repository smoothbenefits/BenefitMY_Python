import reversion

from django.db import models
from ..company import Company
from supplemental_life_insurance_plan import SupplementalLifeInsurancePlan

@reversion.register
class CompanySupplementalLifeInsurancePlan(models.Model):
    supplemental_life_insurance_plan = models.ForeignKey(SupplementalLifeInsurancePlan,
                                                         related_name="company_supplemental_life_insurance_plan")
    
    company = models.ForeignKey(Company,
                                related_name="company_supplemental_life_insurance_plan")

    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
