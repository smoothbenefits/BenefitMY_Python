import datetime
from django.db import models

class CompensationUpdateReason(models.Model):

    name = models.CharField(max_length=256)

    description = models.CharField(max_length=1024, blank=True, null=True)

    created_at = models.DateField(auto_now_add=True, default=datetime.datetime.now)

    updated_at = models.DateField(auto_now=True, default=datetime.datetime.now)
