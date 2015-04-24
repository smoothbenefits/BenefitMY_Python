import reversion

from django.db import models
from django.conf import settings


@reversion.register
class LtdInsurancePlan(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="ltd_insurance_plan")
    attachment = models.CharField(max_length=2048,
                                  blank=True,
                                  null=True)  # doc s3 link

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
