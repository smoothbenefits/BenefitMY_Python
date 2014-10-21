from django.db import models
from company import Company
from user import User
from template import Template
from document_type import DocumentType


class Document(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User)
    template = models.ForeignKey(Template, null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, null=True, blank=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    edited = models.BooleanField(default=False)
