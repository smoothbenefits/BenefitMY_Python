import reversion

from django.db import models
from benefit_type import BenefitType

@reversion.register
class BenefitPlan(models.Model):
    name = models.CharField(max_length=255)
    benefit_type = models.ForeignKey(BenefitType,
                              related_name='benefit_plan')
