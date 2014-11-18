from django.db import models
from django.contrib.auth.models import User


class Signature(models.Model):
    signature = models.TextField()
    user = models.ForeignKey(User, related_name="signature",
                             blank=True,
                             null=True)
    created_at = models.DateTimeField(auto_now_add=True)
