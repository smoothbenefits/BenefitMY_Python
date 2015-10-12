import reversion
from django.db import models
from app.models.person import Person
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
class Employee1095C(models.Model):
    company = models.ForeignKey(Company, related_name="employee_aca_profile_company")
    person = models.ForeignKey(Person, related_name="employee_aca_profile_person")
    safe_harbor = models.CharField(max_length=10, null=True, blank=True)
    period = models.CharField(choices=PERIOD_CHOICES,
                              default='All 12 Months',
                              max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
