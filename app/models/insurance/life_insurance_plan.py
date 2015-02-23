from django.db import models
from django.contrib.auth.models import User

class LifeInsurancePlan(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User,
                             related_name="life_insurance_plan")
    attachment = models.CharField(max_length=2048, blank=True, null=True) #doc s3 link
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
