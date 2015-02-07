from django.db import models
from django.contrib.auth.models import User

S = ["Checking",
     "Saving"]

TYPES = ([(item, item) for item in S])


class DirectDeposit(models.Model):
    routing = models.CharField(max_length=32)
    account = models.CharField(max_length=32)
    account_type = models.TextField(choices=TYPES)

    user = models.ForeignKey(User,
                             related_name="direct_deposit")
