import reversion

from django.db import models
from app.custom_authentication import AuthUser
from company_std_insurance_plan import CompanyStdInsurancePlan
from ..sys_benefit_update_reason import SysBenefitUpdateReason


@reversion.register
class UserCompanyStdInsurancePlan(models.Model):

    user = models.ForeignKey(AuthUser,
                             related_name="user_company_std_insurance_plan")

    company_std_insurance = models.ForeignKey(CompanyStdInsurancePlan,
                                              related_name="std_insurance",
                                              blank=True,
                                              null=True)

    total_premium_per_month = models.DecimalField(max_digits=20,
                                                   decimal_places=10,
                                                   blank=True,
                                                   null=True)

    record_reason = models.ForeignKey(SysBenefitUpdateReason,
                                      related_name="std_update_reason",
                                      blank=True,
                                      null=True)

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)

    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
