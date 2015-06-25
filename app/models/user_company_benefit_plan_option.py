import reversion

from django.db import models
from company_benefit_plan_option import CompanyBenefitPlanOption
from user_company_waived_benefit import UserCompanyWaivedBenefit
from sys_benefit_update_reason import SysBenefitUpdateReason
from app.custom_authentication import AuthUser

@reversion.register
class UserCompanyBenefitPlanOption(models.Model):

    user = models.ForeignKey(AuthUser,
                             related_name="user_company_benefit_plan")
    benefit = models.ForeignKey(
        CompanyBenefitPlanOption,
        related_name="user_company_benefit_plan")

    record_reason = models.ForeignKey(
        SysBenefitUpdateReason, 
        blank=True,
        null=True,
        related_name="health_benefit_update_reason")
    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
