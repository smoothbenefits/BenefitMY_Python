import reversion

from django.db import models
from app.custom_authentication import AuthUser
from app.models.upload import Upload

@reversion.register
class UploadForUser(models.Model):
    upload = models.ForeignKey(Upload, related_name="upload_for_user_upload")
    user_for = models.ForeignKey(AuthUser, related_name="upload_for_user_user_for")
