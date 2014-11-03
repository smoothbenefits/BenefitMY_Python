from django.db import models
from user import User

TYPE = (('step', 'step'),
        ('final', 'final'))


class Signature(models.Model):
    signature = models.TextField()
    signature_type = models.CharField(max_length=30,
                                      choices=TYPE)
    user = models.ForeignKey(User, related_name="signature",
                             blank=True,
                             null=True)
    created_at = models.DateTimeField(auto_now_add=True)
