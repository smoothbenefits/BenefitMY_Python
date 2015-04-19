import reversion

from django.db import models
from django.conf import settings
from company import Company
from document_type import DocumentType
from signature import Signature

@reversion.register
class Document(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    document_type = models.ForeignKey(DocumentType, null=True, blank=True)
    signature = models.ForeignKey(Signature, null=True, blank=True)
    name = models.CharField(max_length=255)
    edited = models.BooleanField(default=False)
    content = models.TextField(null=True,
                               blank=True)
