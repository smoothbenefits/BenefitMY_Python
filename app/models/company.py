import reversion

from django.db import models
from sys_period_definition import SysPeriodDefinition

@reversion.register
class Company(models.Model):
    name = models.CharField(max_length=255)
    pay_period_definition = models.ForeignKey(SysPeriodDefinition,
                                      related_name="sys_pay_period_definition",
                                      blank=True,
                                      null=True)

    def __str__(self):
        return self.name
