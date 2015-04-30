import reversion

from django.db import models
from app.custom_authentication import AuthUser

@reversion.register
class FSA(models.Model):
    primary_amount_per_year = models.DecimalField(max_digits=8, 
                                                  decimal_places=2, 
                                                  null=True)

    dependent_amount_per_year = models.DecimalField(max_digits=8, 
                                                    decimal_places=2, 
                                                    null=True)

    user = models.ForeignKey(AuthUser, related_name="fsa")
    company_fsa_plan = models.ForeignKey(CompanyFsaPlan, related_name="fsa_plan")
    update_reason = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
