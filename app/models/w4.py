from django.db import models
from django.contrib.auth.models import User

class W4(models.Model):
    marriage = models.IntegerField()
    dependencies = models.IntegerField()
    head = models.IntegerField()
    tax_credit = models.IntegerField()
    total_points = models.IntegerField()
    user = models.ForeignKey(User,
                             related_name="w4")
