import reversion

from django.db import models
from app.models.upload import Upload
from app.models.sys_application_feature import SysApplicationFeature

@reversion.register
class UploadApplicationFeature(models.Model):
    upload = models.ForeignKey(Upload, related_name="upload_application_feature_upload")
    application_feature = models.ForeignKey(SysApplicationFeature, related_name="upload_application_feature_app_feature")
    feature_id = models.IntegerField()
