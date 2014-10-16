from django.db import models
from company import Company
from user import User
from template import Template
from document_type import DocumentType


class Document(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User)
    template = models.ForeignKey(Template)
    document_type = models.ForeignKey(DocumentType)
    name = models.TextField()
    content = models.TextField()
    edited = models.BooleanField(default=False)
