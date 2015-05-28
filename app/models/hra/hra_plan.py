import reversion

from django.db import models
from app.custom_authentication import AuthUser

@reversion.register
class HraPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
