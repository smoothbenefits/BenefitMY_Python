from django.db import models

class SysSupplLifeInsuranceCondition(models.Model):

    name = models.CharField(max_length=64)

    description = models.CharField(max_length=1024, blank=True, null=True)
