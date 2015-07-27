from rest_framework import serializers
from app.models.phone import Phone
from hash_pk_serializer_base import HashPkSerializerBase


class PhoneSerializer(HashPkSerializerBase):

    class Meta:
        model = Phone
        fields = ('id', 'phone_type', 'number')
