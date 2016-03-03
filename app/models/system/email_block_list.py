import reversion

from django.db import models
from app.custom_authentication import AuthUser

EMAIL_BLOCK_FEATURE_WORKTIMESHEETNOTIFICATION = 'WorkTimeSheetNotification'


@reversion.register
class EmailBlockList(models.Model):
    email_block_feature = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, related_name="email_block_feature")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
