import reversion
from django.db import models
from app.models.company import Company

PERIODS = ['All 12 Months',
           'Jan',
           'Feb',
           'Mar',
           'Apr',
           'May',
           'June',
           'July',
           'Aug',
           'Sept',
           'Oct',
           'Nov',
           'Dec']

PERIOD_CHOICES = ([(item, item) for item in PERIODS])

@reversion.register
class Company1095C(models.Model):
    company = models.ForeignKey(Company, related_name="company_1095C")
    offer_of_coverage = models.CharField(max_length=2, null=True, blank=True)
    employee_share = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    safe_harbor = models.CharField(max_length=10, null=True, blank=True)
    period = models.CharField(choices=PERIOD_CHOICES,
                              default='All 12 Months',
                              max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
