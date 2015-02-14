from rest_framework import serializers
from app.models.w4 import W4
from hash_pk_serializer_base import HashPkSerializerBase


class W4Serializer(HashPkSerializerBase):

    class Meta:

        model = W4
