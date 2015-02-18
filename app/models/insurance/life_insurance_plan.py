from django.db import models

class LifeInsurancePlan(models.Model):
    name = models.CharField(max_length=255)
    attachment = models.CharField(max_length=2048, blank=True, null=True) #doc s3 link
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
