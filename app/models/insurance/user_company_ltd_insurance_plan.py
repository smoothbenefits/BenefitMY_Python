import reversion

from django.db import models
from company_ltd_insurance_plan import CompanyLtdInsurancePlan

from django.contrib.auth.models import User


@reversion.register
class UserCompanyLtdInsurancePlan(models.Model):

    user = models.ForeignKey(User,
                             related_name="user_company_ltd_insurance_plan")
    company_ltd_insurance = models.ForeignKey(
        CompanyLtdInsurancePlan,
        related_name="ltd_insurance")

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
