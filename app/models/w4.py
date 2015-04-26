import reversion

from django.db import models
from django.conf import settings

@reversion.register
class W4(models.Model):
    marriage = models.IntegerField()
    dependencies = models.IntegerField()
    head = models.IntegerField()
    tax_credit = models.IntegerField()
    calculated_points = models.IntegerField()
    user_defined_points = models.IntegerField(blank=True, null=True)
    extra_amount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="w4")
