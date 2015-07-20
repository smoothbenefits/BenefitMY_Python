import reversion

from django.db import models
from company import Company
from benefit_type import BenefitType
from app.custom_authentication import AuthUser
from sys_benefit_update_reason import SysBenefitUpdateReason

@reversion.register
class UserCompanyWaivedBenefit(models.Model):

    user = models.ForeignKey(AuthUser)
    company = models.ForeignKey(Company)
    benefit_type = models.ForeignKey(BenefitType)
    reason = models.CharField(max_length=2048,
                              null=True,
                              blank=True)

    record_reason = models.ForeignKey(
        SysBenefitUpdateReason,
        blank=True,
        null=True,
        related_name="health_benefit_waive_update_reason")
    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
