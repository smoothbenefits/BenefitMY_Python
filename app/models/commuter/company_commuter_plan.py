import reversion

from django.db import models

from ..company import Company

DEDUCTION_PERIOD_MONTHLY = 'Monthly'
DEDUCTION_PERIOD_PAY_PERIOD = 'PerPayPeriod'
DEDUCTION_PERIOD_OPTIONS = ([(item, item) for item in [DEDUCTION_PERIOD_MONTHLY, DEDUCTION_PERIOD_PAY_PERIOD]])


@reversion.register
class CompanyCommuterPlan(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    enable_transit_benefit = models.BooleanField(default=False)
    enable_parking_benefit = models.BooleanField(default=False)

    employer_contribution = models.DecimalField(max_digits=20, decimal_places=10)

    deduction_period = models.CharField(max_length=30, choices=DEDUCTION_PERIOD_OPTIONS)

    company = models.ForeignKey(
        Company,
        related_name="company_commuter_plan")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
