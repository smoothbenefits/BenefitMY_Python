from rest_framework import serializers
from app.models.upload_audience import UploadAudience
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from app.serializers.upload_serializer import UploadPostSerializer, UploadSerializer
from app.serializers.company_serializer import ShallowCompanySerializer


class UploadAudienceSerializer(HashPkSerializerBase):
    user_for = HashField(source="user_for.id")
    company = ShallowCompanySerializer()
    upload = UploadSerializer()
    class Meta:
        model = UploadAudience


class UploadAudiencePostSerializer(HashPkSerializerBase):
    class Meta:
        model = UploadAudience
