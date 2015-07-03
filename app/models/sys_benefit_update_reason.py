from django.db import models
from sys_benefit_update_reason_category import SysBenefitUpdateReasonCategory

class SysBenefitUpdateReason(models.Model):

    name = models.CharField(max_length=256)

    description = models.CharField(max_length=1024, blank=True, null=True)

    category = models.ForeignKey(SysBenefitUpdateReasonCategory,
        related_name="benefit_update_reason_category",
        blank=True,
        null=True)

    detail_required = models.BooleanField(default=False)
