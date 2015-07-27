import reversion

from django.db import models
from company_life_insurance_plan import CompanyLifeInsurancePlan

from app.custom_authentication import AuthUser
from ..person import Person
from ..sys_benefit_update_reason import SysBenefitUpdateReason

@reversion.register
class UserCompanyLifeInsurancePlan(models.Model):

    user = models.ForeignKey(AuthUser,
                             related_name="user_company_life_insurance_plan")

    company_life_insurance = models.ForeignKey(CompanyLifeInsurancePlan,
                                               related_name="life_insurance",
                                               blank=True,
                                               null=True)

    person = models.ForeignKey(Person,
                               related_name="life_insurance")

    # for extend life insurance only
    insurance_amount = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True)

    record_reason = models.ForeignKey(SysBenefitUpdateReason,
                                      related_name="basic_life_update_reason",
                                      blank=True,
                                      null=True)

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)

    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
