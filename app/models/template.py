from django.db import models
from company import Company
from document_type import DocumentType


class Template(models.Model):
    company = models.ForeignKey(Company)
    document_type = models.ForeignKey(DocumentType)
    name = models.TextField()
    content = models.TextField()
