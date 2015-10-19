import reversion

from django.db import models
from company import Company
from document_type import DocumentType

@reversion.register
class Template(models.Model):
    company = models.ForeignKey(Company,
                                related_name="template")
    name = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
