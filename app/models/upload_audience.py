import reversion

from django.db import models
from django.conf import settings
from app.models.company import Company
from app.models.upload import Upload

@reversion.register
class UploadAudience(models.Model):
    company = models.ForeignKey(Company, related_name="upload_audience_company")
    upload = models.ForeignKey(Upload, related_name="upload_audience_upload")
    user_for = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="upload_audience_user_for", null=True, blank=True)
