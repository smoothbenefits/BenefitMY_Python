from rest_framework import serializers
from app.models.user_bank_account import UserBankAccount
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField


class UserBankAccountSerializer(HashPkSerializerBase):

    user = HashField(source="user.id")
    class Meta:
        model = UserBankAccount

class UserBankAccountPostSerializer(HashPkSerializerBase):

    class Meta:
		model = UserBankAccount
