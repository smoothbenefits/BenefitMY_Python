import reversion

from django.db import models
from company_life_insurance_plan import CompanyLifeInsurancePlan

from django.contrib.auth.models import User
from ..person import Person

@reversion.register
class UserCompanyLifeInsurancePlan(models.Model):

    user = models.ForeignKey(User,
                             related_name="user_company_life_insurance_plan")
    company_life_insurance = models.ForeignKey(
        CompanyLifeInsurancePlan,
        related_name="life_insurance")

    person = models.ForeignKey(Person,
                               related_name="life_insurance")
    # for extend life insurance only
    insurance_amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
