import reversion

from django.db import models
from company import Company
from app.custom_authentication import AuthUser
from sys_benefit_update_reason import SysBenefitUpdateReason
from company_fsa_plan import CompanyFsaPlan

@reversion.register
class UserWaivedCompanyFsa(models.Model):

    user = models.ForeignKey(AuthUser, related_name='user_waived_fsa_user')

    company = models.ForeignKey(Company, related_name='user_waived_fsa_company')

    company_ltd_insurance = models.ForeignKey(CompanyFsaPlan,
                                              related_name='user_waived_fsa')

    reason = models.CharField(max_length=2048,
                              null=True,
                              blank=True)

    record_reason = models.ForeignKey(
        SysBenefitUpdateReason,
        blank=True,
        null=True,
        related_name="fsa_waive_update_reason")

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)

    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
