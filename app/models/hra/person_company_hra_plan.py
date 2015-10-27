import reversion

from django.db import models
from company_hra_plan import CompanyHraPlan

from app.custom_authentication import AuthUser
from ..person import Person
from ..sys_benefit_update_reason import SysBenefitUpdateReason

@reversion.register
class PersonCompanyHraPlan(models.Model):

    company_hra_plan = models.ForeignKey(
        CompanyHraPlan,
        blank=True,
        null=True,
        related_name="person_company_hra_plan")

    person = models.ForeignKey(
        Person,
        related_name="person_company_hra_plan")

    record_reason = models.ForeignKey(
        SysBenefitUpdateReason,
        blank=True,
        null=True,
        related_name="hra_update_reason")
    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
