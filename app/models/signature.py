import reversion

from django.db import models
from app.custom_authentication import AuthUser

@reversion.register
class Signature(models.Model):
    signature = models.TextField()
    signature_type = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(AuthUser,
                             related_name="signature",
                             blank=True,
                             null=True)
    created_at = models.DateTimeField(auto_now_add=True)
