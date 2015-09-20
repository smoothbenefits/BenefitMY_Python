from django.db import models


class SysApplicationFeature(models.Model):
    feature = models.CharField(max_length=32)
    def __str__(self):
        return self.feature
