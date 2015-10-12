import reversion

from django.db import models

from company_extra_benefit_plan import CompanyExtraBenefitPlan
from ..person import Person
from ..sys_benefit_update_reason import SysBenefitUpdateReason


@reversion.register
class PersonCompanyExtraBenefitPlan(models.Model):

    company_plan = models.ForeignKey(
        CompanyExtraBenefitPlan,
        related_name="person_company_extra_benefit_plan")

    person = models.ForeignKey(
        Person,
        related_name="person_company_extra_benefit_plan")

    record_reason = models.ForeignKey(
        SysBenefitUpdateReason,
        blank=True,
        null=True,
        related_name="extra_benefits_update_reason")
    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
