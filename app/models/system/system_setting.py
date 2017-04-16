from django.db import models


class SystemSetting(models.Model):
    name = models.CharField(max_length=127, unique=True)
    value = models.CharField(max_length=1023, blank=True, null=True)

    def __str__(self):
        return self.name
