from django.db import models
from user import User

class W4(models.Model):
    marriage = models.IntegerField()
    dependencies = models.IntegerField()
    head = models.BooleanField()
    tax_credit = models.BooleanField()
    total_points = models.IntegerField()
    user = models.ForeignKey(User,
                             related_name="employment_authorization")
