from django.db import models
from django.contrib.auth.models import User

S = ["Checking",
     "Saving"]

TYPES = ([(item, item) for item in S])


class DirectDeposit(models.Model):
    routing = models.CharField(max_length=32)
    account = models.CharField(max_length=32)
    account_type = models.TextField(choices=TYPES)
    bank_name = models.CharField(max_length=128, blank=True, null=True)
    attachment = models.CharField(max_length=2048, blank=True, null=True)    # S3 link
    user = models.ForeignKey(User,
                             related_name="direct_deposit")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
