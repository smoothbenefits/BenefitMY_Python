import reversion
from django.db import models
from app.models.company import Company

PERIODS = ['All 12 Months', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
           'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

PERIOD_CHOICES = ([(item, item) for item in PERIODS])

@reversion.register
class Company1094CMonthlyMemberInfo(models.Model):
    company = models.ForeignKey(Company, related_name="company_1094C_monthly")
    minimum_essential_coverage = models.BooleanField(default=False)
    fulltime_employee_count = models.PositiveIntegerField(default=0)
    total_employee_count = models.PositiveIntegerField(default=0)
    aggregated_group = models.BooleanField(default=False)
    section_4980h_transition_relief = models.BooleanField(default=False)
    period = models.CharField(choices=PERIOD_CHOICES,
                              default='All 12 Months',
                              max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
