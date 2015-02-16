from rest_framework import serializers
from app.models.direct_deposit import DirectDeposit
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from user_bank_account_serializer import UserBankAccountSerializer


class DirectDepositSerializer(HashPkSerializerBase):

	user = HashField(source="user.id")

	class Meta:
		model = DirectDeposit

class DirectDepositPostSerializer(HashPkSerializerBase):

	class Meta:
		model = DirectDeposit

    bank_account = UserBankAccountSerializer()

