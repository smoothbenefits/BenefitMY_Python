import reversion

from datetime import datetime
from django.db import models
from app.custom_authentication import AuthUser
from company_fsa_plan import CompanyFsaPlan
from ..sys_benefit_update_reason import SysBenefitUpdateReason

@reversion.register
class FSA(models.Model):
    primary_amount_per_year = models.DecimalField(max_digits=8,
                                                  decimal_places=2,
                                                  null=True)

    dependent_amount_per_year = models.DecimalField(max_digits=8,
                                                    decimal_places=2,
                                                    null=True)

    user = models.ForeignKey(AuthUser, related_name="fsa_user")

    company_fsa_plan = models.ForeignKey(CompanyFsaPlan,
                                         related_name="fsa_company_fsa_plan",
                                         blank=True,
                                         null=True)

    update_reason = models.CharField(max_length=1024, blank=True, null=True)

    record_reason = models.ForeignKey(SysBenefitUpdateReason,
                                      related_name="fsa_update_reason",
                                      blank=True,
                                      null=True)

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now)

    updated_at = models.DateTimeField(auto_now=True, default=datetime.now)
