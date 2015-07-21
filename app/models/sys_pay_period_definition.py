from django.db import models


class SysPayPeriodDefinition(models.Model):
    name = models.CharField(max_length=32)
    month_factor = models.FloatField()
