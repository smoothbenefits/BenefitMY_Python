from rest_framework import serializers
from app.models.direct_deposit import DirectDeposit
from user_bank_account_serializer import UserBankAccountSerializer


class DirectDepositSerializer(serializers.ModelSerializer):

    bank_account = UserBankAccountSerializer()

    class Meta:
        model = DirectDeposit
