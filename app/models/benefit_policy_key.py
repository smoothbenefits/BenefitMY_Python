from django.db import models

import reversion

@reversion.register
class BenefitPolicyKey(models.Model):
    name = models.CharField(max_length=255)

