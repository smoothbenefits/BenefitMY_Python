import reversion

from django.db import models
from django.contrib.auth.models import User


@reversion.register
class LtdInsurancePlan(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User,
                             related_name="ltd_insurance_plan")
    attachment = models.CharField(max_length=2048,
                                  blank=True,
                                  null=True)  # doc s3 link

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
