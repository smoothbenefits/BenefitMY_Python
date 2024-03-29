import datetime
import reversion

from django.db import models
from person import Person
from company import Company

@reversion.register
class EmployeeTimeTracking(models.Model):

    actual_hour_month = models.DateField()

    actual_hour_per_month = models.DecimalField(max_digits=12, decimal_places=4,
                                                    blank=True, null=True)

    person = models.ForeignKey(Person,
                               related_name="employee_timetracking_person")

    company = models.ForeignKey(Company,
                                related_name="employee_timetracking_company")

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)

    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    class Meta:
        unique_together = ('person', 'company')
