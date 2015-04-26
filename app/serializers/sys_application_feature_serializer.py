from app.models.sys_application_feature import SysApplicationFeature

from hash_pk_serializer_base import HashPkSerializerBase


class SysApplicationFeatureSerializer(HashPkSerializerBase):

    class Meta:
        model = SysApplicationFeature
