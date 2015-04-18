import reversion

from django.db import models
from company_std_insurance_plan import CompanyStdInsurancePlan

from django.contrib.auth.models import User


@reversion.register
class UserCompanyStdInsurancePlan(models.Model):

    user = models.ForeignKey(User,
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
