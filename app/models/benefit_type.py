from django.db import models


class BenefitType(models.Model):
    name = models.TextField()
    display_priority = models.IntegerField()
