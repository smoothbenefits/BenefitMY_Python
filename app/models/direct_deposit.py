import reversion

from django.db import models
from app.custom_authentication import AuthUser
from user_bank_account import UserBankAccount

@reversion.register
class DirectDeposit(models.Model):
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True)

    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    bank_account = models.ForeignKey(UserBankAccount,
                             related_name="direct_deposit")

    user = models.ForeignKey(AuthUser,
                             related_name="direct_deposit")

    remainder_of_all = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
