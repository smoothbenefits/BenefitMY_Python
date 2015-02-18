from rest_framework import serializers
from app.models.user_bank_account import UserBankAccount
from hash_pk_serializer_base import HashPkSerializerBase


class UserBankAccountSerializer(HashPkSerializerBase):

    class Meta:
        model = UserBankAccount
