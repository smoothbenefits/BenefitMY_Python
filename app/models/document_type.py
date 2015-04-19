import reversion

from django.db import models

@reversion.register
class DocumentType(models.Model):
    name = models.CharField(max_length=255)
    default_content = models.TextField(blank=True, null=True)
