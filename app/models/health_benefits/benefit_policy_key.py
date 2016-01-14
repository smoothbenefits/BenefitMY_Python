import reversion

from django.db import models

@reversion.register
class BenefitPolicyKey(models.Model):
    name = models.CharField(max_length=255)
    rank = models.IntegerField(default=9999)
