from rest_framework import serializers
from app.models.upload_application_feature import UploadApplicationFeature
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from app.serializers.upload_serializer import UploadPostSerializer, UploadSerializer
from app.serializers.sys_application_feature_serializer import SysApplicationFeatureSerializer


class UploadAppliactionFeatureSerializer(HashPkSerializerBase):
    upload = UploadSerializer()
    application_feature = SysApplicationFeatureSerializer()
    class Meta:
        model = UploadApplicationFeature


class UploadAppliactionFeaturePostSerializer(HashPkSerializerBase):
    class Meta:
        model = UploadApplicationFeature
