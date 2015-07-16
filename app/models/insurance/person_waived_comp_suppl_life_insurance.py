import reversion

from django.db import models
from ..company import Company
from ..person import Person
from ..sys_benefit_update_reason import SysBenefitUpdateReason
from comp_suppl_life_insurance_plan import CompSupplLifeInsurancePlan

@reversion.register
class PersonWaivedCompSupplLifeInsurance(models.Model):

    person = models.ForeignKey(Person, related_name='person_waived_suppl_life_person')

    company = models.ForeignKey(Company, related_name='person_waived_suppl_life_comp')

    company_supplemental_life_insurance_plan = models.ForeignKey(CompSupplLifeInsurancePlan,
                                               related_name='person_waived_suppl_life')

    reason = models.CharField(max_length=2048,
                              null=True,
                              blank=True)

    record_reason = models.ForeignKey(
        SysBenefitUpdateReason,
        blank=True,
        null=True,
        related_name="suppl_life_waive_update_reason")

    record_reason_note = models.CharField(max_length=512, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)

    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
