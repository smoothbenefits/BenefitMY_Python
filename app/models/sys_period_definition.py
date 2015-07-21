from django.db import models


class SysPeriodDefinition(models.Model):
    name = models.CharField(max_length=32)
    month_factor = models.FloatField()
