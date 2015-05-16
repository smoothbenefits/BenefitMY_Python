import reversion

from django.db import models
from ..sys_suppl_life_insurance_condition import SysSupplLifeInsuranceCondition
from supplemental_life_insurance_plan import SupplementalLifeInsurancePlan

BIND_TYPES = (('self', 'Self'),
             ('spouse', 'Spouse'),
             ('dependent', 'Dependent'))

@reversion.register
class SupplementalLifeInsurancePlanRate(models.Model):
    supplemental_life_insurance_plan = models.ForeignKey(SupplementalLifeInsurancePlan,
                                                         related_name="supplemental_life_insurance_plan_rate",
                                                         blank=True,
                                                         null=True)
    age_min = models.SmallIntegerField(blank=True, 
                                       null=True,
                                       verbose_name="Min value of age. Null for children")

    age_max = models.SmallIntegerField(blank=True, 
                                       null=True, 
                                       verbose_name="Max value of age. Null for children")

    bind_type = models.CharField(max_length=32,
                                 choices=BIND_TYPES)

    rate = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               blank=False,
                               null=False)

    condition = models.ForeignKey(SysSupplLifeInsuranceCondition,
                                      related_name="supplemental_life_insurance_plan_rate")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
