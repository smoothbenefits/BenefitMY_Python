import datetime
import reversion

from django.db import models
from person import Person
from compensation_update_reason import CompensationUpdateReason

@reversion.register
class EmployeeCompensation(models.Model):

    person = models.ForeignKey(Person, related_name="employee_compensation_person",
                               blank=True, null=True, db_index=True)

    annual_base_salary = models.DecimalField(max_digits=12,
                                             decimal_places=2,
                                             blank=True,
                                             null=True)

    increase_percentage = models.DecimalField(max_digits=5,
                                              decimal_places=2,
                                              blank=True,
                                              null=True)

    reason = models.ForeignKey(CompensationUpdateReason,
                               related_name="employee_compensation",
                               blank=True,
                               null=True)

    effective_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now, 
                                      db_index=True)

    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
