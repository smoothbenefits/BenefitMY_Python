import reversion

from django.db import models
from app.custom_authentication import AuthUser
from app.models.company import Company
from app.models.upload import Upload

@reversion.register
class UploadAudience(models.Model):
    company = models.ForeignKey(Company, related_name="upload_audience_company")
    upload = models.ForeignKey(Upload, related_name="upload_audience_upload")
    user_for = models.ForeignKey(AuthUser, related_name="upload_audience_user_for", null=True, blank=True)
