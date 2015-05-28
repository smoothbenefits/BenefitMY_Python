import reversion

from django.db import models
from app.custom_authentication import AuthUser
from company_ltd_insurance_plan import CompanyLtdInsurancePlan

@reversion.register
class UserCompanyLtdInsurancePlan(models.Model):

    user = models.ForeignKey(AuthUser,
                             related_name="user_company_ltd_insurance_plan")
    company_ltd_insurance = models.ForeignKey(
        CompanyLtdInsurancePlan,
        related_name="ltd_insurance")

    total_premium_per_period = models.DecimalField(max_digits=10, 
                                                   decimal_places=2, 
                                                   blank=True, 
                                                   null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
