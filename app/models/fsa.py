import reversion

from django.db import models
from django.conf import settings

@reversion.register
class FSA(models.Model):
    primary_amount_per_year = models.DecimalField(
        max_digits=8, decimal_places=2, null=True)
    dependent_amount_per_year = models.DecimalField(
        max_digits=8, decimal_places=2, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="fsa")

    update_reason = models.CharField(max_length=1024, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      blank=True,
                                      null=True)
