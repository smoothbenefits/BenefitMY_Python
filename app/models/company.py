import reversion

from django.db import models
from sys_period_definition import SysPeriodDefinition

@reversion.register
class Company(models.Model):
    name = models.CharField(max_length=255)
    pay_period_definition = models.ForeignKey(SysPeriodDefinition,
                                      related_name="sys_pay_period_definition",
                                      default=2)
    ein = models.CharField(max_length=30, null=True, blank=True)

    offer_of_coverage_code = models.CharField(max_length=10, null=True, blank=True)

    open_enrollment_month = models.IntegerField(null=True, blank=True)

    open_enrollment_day = models.IntegerField(null=True, blank=True)

    open_enrollment_length_in_days = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
