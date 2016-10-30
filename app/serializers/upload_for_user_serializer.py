from rest_framework import serializers
from app.models.upload_for_user import UploadForUser
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from app.serializers.upload_serializer import UploadPostSerializer, UploadSerializer


class UploadForUserSerializer(HashPkSerializerBase):
    user_for = HashField(source="user_for.id")
    upload = UploadSerializer()
    class Meta:
        model = UploadForUser


class UploadForUserPostSerializer(HashPkSerializerBase):
    class Meta:
        model = UploadForUser
