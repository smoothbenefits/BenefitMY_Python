import reversion

from django.db import models
from app.custom_authentication import AuthUser
from app.models.company import Company

@reversion.register
class Upload(models.Model):
    user = models.ForeignKey(AuthUser, related_name="user_upload")
    company = models.ForeignKey(Company, related_name="company_upload")
    S3 = models.CharField(max_length=2048)    # S3 link
    file_name = models.CharField(max_length=2048, blank=True, null=True)
    file_type = models.CharField(max_length=128, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
