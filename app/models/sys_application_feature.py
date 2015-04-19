from django.db import models


class SysApplicationFeature(models.Model):
    feature = models.CharField(max_length=32)
