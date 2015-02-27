from rest_framework import serializers
from app.models.signature import Signature
from hash_pk_serializer_base import HashPkSerializerBase


class SignatureSerializer(HashPkSerializerBase):

    class Meta:

        model = Signature
