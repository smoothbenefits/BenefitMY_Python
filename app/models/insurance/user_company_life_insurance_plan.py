from django.db import models
from company_life_insurance_plan import CompanyLifeInsurancePlan

from django.contrib.auth.models import User
from person import Person


class UserCompanyLifeInsurancePlan(models.Model):

    user = models.ForeignKey(User,
                             related_name="user_company_life_insurance_plan")
    life_insurance = models.ForeignKey(
        CompanyLifeInsurancePlan,
        related_name="life_insurance")

    person = models.ForeignKey(Person,
                               related_name="life_insurance")
    insurance_amount = models.DecimalField(
        max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
