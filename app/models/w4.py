from django.db import models


class w4(models.Model):
    marriage = models.IntegerField()
    dependencies = models.IntegerField()
    head = models.BooleanField()
    tax_credit = models.BooleanField()
    total_points = models.IntegerField()
