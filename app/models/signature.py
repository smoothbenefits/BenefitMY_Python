import reversion

from django.db import models
from django.conf import settings

@reversion.register
class Signature(models.Model):
    signature = models.TextField()
    signature_type = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             related_name="signature",
                             blank=True,
                             null=True)
    created_at = models.DateTimeField(auto_now_add=True)
