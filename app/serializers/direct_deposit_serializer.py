from rest_framework import serializers
from app.models.direct_deposit import DirectDeposit


class DirectDepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = DirectDeposit
