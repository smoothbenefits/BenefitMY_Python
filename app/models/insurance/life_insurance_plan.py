import reversion

from django.db import models
from django.conf import settings

INSURANCE_TYPES = ([(item, item) for item in ['Basic', 'Extended']])

@reversion.register
class LifeInsurancePlan(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="life_insurance_plan")
    attachment = models.CharField(max_length=2048,
                                  blank=True,
                                  null=True) #doc s3 link
    insurance_type = models.CharField(max_length=16,
                              choices=INSURANCE_TYPES,
                              null=True,
                              blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
