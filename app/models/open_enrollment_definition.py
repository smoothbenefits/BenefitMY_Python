import reversion

from django.db import models
from app.models.company import Company

@reversion.register
class OpenEnrollmentDefinition(models.Model):
    company = models.ForeignKey(Company,
                             related_name="employment_authorization",
                             unique=True)

    start_month = models.IntegerField()

    start_day = models.IntegerField()

    end_month = models.IntegerField()

    end_day = models.IntegerField()
