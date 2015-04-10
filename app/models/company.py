from django.db import models

import reversion

@reversion.register
class Company(models.Model):
    name = models.CharField(max_length=255)
