import reversion

from django.db import models

@reversion.register
class BenefitPolicyType(models.Model):
    name = models.CharField(max_length=255)

