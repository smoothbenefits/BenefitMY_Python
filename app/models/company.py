from django.db import models


class Company(models.Model):
    name = models.TextField()
    default_tz = models.TextField()
