from rest_framework import serializers
from app.models.upload import Upload
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField


class UploadSerializer(HashPkSerializerBase):
    user = HashField(source="user.id")
    company = HashField(source="company.id")
    class Meta:
        model = Upload


class UploadPostSerializer(HashPkSerializerBase):
    class Meta:
        model = Upload
