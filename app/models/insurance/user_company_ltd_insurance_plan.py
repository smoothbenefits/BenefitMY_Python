import reversion

from django.db import models
from app.custom_authentication import AuthUser
from company_ltd_insurance_plan import CompanyLtdInsurancePlan
from ..sys_benefit_update_reason import SysBenefitUpdateReason

@reversion.register
class UserCompanyLtdInsurancePlan(models.Model):

    user = models.ForeignKey(AuthUser,
                             related_name="user_company_ltd_insurance_plan")

    company_ltd_insurance = models.ForeignKey(CompanyLtdInsurancePlan,
                                              related_name="ltd_insurance",
                                              blank=True,
                                              null=True)

    total_premium_per_period = models.DecimalField(max_digits=10,
                                                   decimal_places=2,
                                                   blank=True,
                                                   null=True)

    record_reason = models.ForeignKey(SysBenefitUpdateReason,
                                      related_name="ltd_update_reason",
                                      blank=True,
                                      null=True)

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)

    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
