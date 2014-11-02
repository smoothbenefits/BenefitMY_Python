from django.db import models

TYPE = (('step', 'step'),
        ('final', 'final'))


class Signature(models.Model):
    signature = models.TextField()
    signature_type = models.CharField(max_length=30,
                                      choices=TYPE)
    user = models.ForeignKey(User, related_name="signature")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
