from django.db import models

PERIOD_WEEKLY = 'Weekly'
PERIOD_BIWEEKLY = 'Bi-Weekly'
PERIOD_SEMIMONTHLY = 'Semi-Monthly'
PERIOD_MONTHLY = 'Monthly'
PERIOD_QUARTERLY = 'Quarterly'
PERIOD_ANNUALLY = 'Annually'
PERIOD_PERDIEM = 'Per Diem'

class SysPeriodDefinition(models.Model):
    name = models.CharField(max_length=32)
    month_factor = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.name
