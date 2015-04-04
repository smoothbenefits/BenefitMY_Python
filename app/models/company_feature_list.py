from django.db import models


class CompanyFeatureList(models.Model):
    feature = models.CharField(max_length=32)
