from django.db import models
from django.contrib.auth.models import User

S = ["Checking",
     "Saving"]

TYPES = ([(item, item) for item in S])


class DirectDeposit(models.Model):
    routing1 = models.CharField(max_length=32)
    account1 = models.CharField(max_length=32)
    account_type1 = models.TextField(choices=TYPES)
    bank_name1 = models.CharField(max_length=128, blank=True, null=True)
    attachment1 = models.CharField(max_length=2048, blank=True, null=True)    # S3 link
    amount1= models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True)
    percentage1= models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    routing2 = models.CharField(max_length=32, blank=True, null=True)
    account2 = models.CharField(max_length=32, blank=True, null=True)
    account_type2 = models.TextField(choices=TYPES, blank=True, null=True)
    bank_name2 = models.CharField(max_length=128, blank=True, null=True)
    attachment2 = models.CharField(max_length=2048, blank=True, null=True)    # S3 link
    amount2= models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True)
    percentage2= models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    user = models.ForeignKey(User,
                             unique=True,
                             related_name="direct_deposit")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
