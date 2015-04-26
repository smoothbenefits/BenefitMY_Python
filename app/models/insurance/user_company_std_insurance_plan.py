import reversion

from django.db import models
from django.conf import settings
from company_std_insurance_plan import CompanyStdInsurancePlan



@reversion.register
class UserCompanyStdInsurancePlan(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="user_company_std_insurance_plan")
    company_std_insurance = models.ForeignKey(
        CompanyStdInsurancePlan,
        related_name="std_insurance")

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
