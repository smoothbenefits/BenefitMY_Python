from django.db import models
from document import Document


class DocumentField(models.Model):
    document_id = models.ForeignKey(Document, related_name="document_field")
    name = models.CharField(max_length=255)
    value = models.TextField()
