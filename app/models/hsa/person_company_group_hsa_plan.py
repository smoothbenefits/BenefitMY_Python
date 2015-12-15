import reversion

from django.db import models
from app.person import Person
from company_group_hsa_plan import CompanyGroupHsaPlan
from app.sys_benefit_update_reason import SysBenefitUpdateReason

@reversion.register
class PersonCompanyGroupHsaPlan(models.Model):
    amount_per_year = models.DecimalField(max_digits=8,
                                          decimal_places=2,
                                          blank=True,
                                          null=True)

    person = models.ForeignKey(Person, related_name="hsa_plan_person")

    company_group_hsa_plan = models.ForeignKey(CompanyGroupHsaPlan,
                                         related_name="company_group_hsa_plan",
                                         blank=True,
                                         null=True)

    update_reason = models.CharField(max_length=1024, blank=True, null=True)

    record_reason = models.ForeignKey(SysBenefitUpdateReason,
                                      related_name="hsa_update_reason",
                                      blank=True,
                                      null=True)

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
