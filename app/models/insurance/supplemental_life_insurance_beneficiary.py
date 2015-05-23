import reversion

from django.db import models
from person_comp_suppl_life_insurance_plan import PersonCompSupplLifeInsurancePlan

TIER = ([(item, item) for item in ['1', '2']])

@reversion.register
class SupplementalLifeInsuranceBeneficiary(models.Model):

    first_name = models.CharField(max_length=255, null=True)

    middle_name = models.CharField(max_length=255, null=True, blank=True)

    last_name = models.CharField(max_length=255, null=True)

    relationship = models.CharField(max_length=30, null=True)

    email = models.EmailField(max_length=255, null=True, blank=True)

    phone = models.CharField(max_length=32, null=True, blank=True)

    person_comp_suppl_life_insurance_plan = models.ForeignKey(PersonCompSupplLifeInsurancePlan,
                                                              related_name='suppl_life_insurance_beneficiary',
                                                              blank=True,
                                                              null=True)

    percentage = models.DecimalField(max_digits=5,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)

    tier = models.CharField(max_length=1,
                            choices=TIER,
                            null=True,
                            blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, null=True)
