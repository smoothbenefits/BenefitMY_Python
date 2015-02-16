from rest_framework import serializers
from app.models.user_bank_account import UserBankAccount


class UserBankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBankAccount
