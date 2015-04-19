import reversion

from django.db import models

@reversion.register
class Company(models.Model):
    name = models.CharField(max_length=255)
