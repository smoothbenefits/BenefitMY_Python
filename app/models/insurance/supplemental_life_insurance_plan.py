import reversion

from django.db import models

@reversion.register
class SupplementalLifeInsurancePlan(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
