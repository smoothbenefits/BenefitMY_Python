from django.db import models

class SysBenefitUpdateReasonCategory(models.Model):

    name = models.CharField(max_length=256)

    description = models.CharField(max_length=1024, blank=True, null=True)

    rank = models.PositiveSmallIntegerField(blank=True, null=True)
