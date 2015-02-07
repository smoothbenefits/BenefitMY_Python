from django.db import models
from company_life_insurance_plan import CompanyLifeInsurancePlan

from django.contrib.auth.models import User


class UserCompanyLifeInsurancePlan(models.Model):

    user = models.ForeignKey(User,
                             related_name="user_company_life_insurance_plan")
    life_insurance = models.ForeignKey(
        CompanyLifeInsurancePlan,
        related_name="user_company_life_insurance_plan")
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
