import reversion

from django.db import models
from app.custom_authentication import AuthUser
from company import Company
from signature import Signature
from upload import Upload


@reversion.register
class Document(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(AuthUser)
    signature = models.ForeignKey(Signature, null=True, blank=True)
    name = models.CharField(max_length=255)
    edited = models.BooleanField(default=False)
    content = models.TextField(null=True,
                               blank=True)
    upload = models.ForeignKey(Upload,
                               blank=True,
                               null=True,
                               related_name='document_uploads')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
