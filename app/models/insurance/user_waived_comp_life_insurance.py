import reversion

from django.db import models
from ..company import Company
from ..sys_benefit_update_reason import SysBenefitUpdateReason
from app.custom_authentication import AuthUser
from company_life_insurance_plan import CompanyLifeInsurancePlan

@reversion.register
class UserWaivedCompLifeInsurance(models.Model):

    user = models.ForeignKey(AuthUser, related_name='user_waived_life_user')

    company = models.ForeignKey(Company, related_name='user_waived_life_company')

    company_life_insurance = models.ForeignKey(CompanyLifeInsurancePlan,
                                              related_name='user_waived_basic_life')

    reason = models.CharField(max_length=2048,
                              null=True,
                              blank=True)

    record_reason = models.ForeignKey(
        SysBenefitUpdateReason,
        blank=True,
        null=True,
        related_name="basic_life_waive_update_reason")

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)

    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
