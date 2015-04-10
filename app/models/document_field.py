from django.db import models
from document import Document

import reversion

@reversion.register
class DocumentField(models.Model):
    document = models.ForeignKey(Document, related_name="fields")
    name = models.CharField(max_length=255)
    value = models.TextField()
