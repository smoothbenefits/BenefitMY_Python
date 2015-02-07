from django.db import models

class LifeInsurancePlan(models.Model):
    name = models.CharField(max_length=255)
    doc = models.CharField(max_length=1024, blank=True, null=True) #doc link
