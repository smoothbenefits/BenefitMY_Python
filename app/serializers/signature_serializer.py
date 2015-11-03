from rest_framework import serializers
from app.models.signature import Signature
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField


class SignatureSerializer(HashPkSerializerBase):
    user = HashField(source="user.id")

    class Meta:
        model = Signature


class SignaturePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signature
