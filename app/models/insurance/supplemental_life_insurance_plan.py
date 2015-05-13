import reversion

from django.db import models

@reversion.register
class SupplementalLifeInsurancePlan(models.Model):
    name = models.CharField(max_length=255)

    use_employee_age_for_spouse = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
