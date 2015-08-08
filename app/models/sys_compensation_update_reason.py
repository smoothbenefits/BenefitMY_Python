import datetime
import reversion
from django.db import models

@reversion.register
class SysCompensationUpdateReason(models.Model):

    name = models.CharField(max_length=256)

    created_at = models.DateField(auto_now_add=True, default=datetime.datetime.now)

    updated_at = models.DateField(auto_now=True, default=datetime.datetime.now)
