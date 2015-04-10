from django.db import models
from django.contrib.auth.models import User
from company import Company
from document_type import DocumentType
from signature import Signature

import reversion

@reversion.register
class Document(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User)
    document_type = models.ForeignKey(DocumentType, null=True, blank=True)
    signature = models.ForeignKey(Signature, null=True, blank=True)
    name = models.CharField(max_length=255)
    edited = models.BooleanField(default=False)
    content = models.TextField(null=True,
                               blank=True)
