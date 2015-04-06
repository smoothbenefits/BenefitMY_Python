from rest_framework import serializers
from app.models.upload import Upload
from hash_pk_serializer_base import HashPkSerializerBase


class UploadSerializer(HashPkSerializerBase):

    class Meta:
        model = Upload