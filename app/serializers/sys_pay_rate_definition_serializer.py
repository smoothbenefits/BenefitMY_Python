from app.models.sys_pay_rate_definition import SysPayRateDefinition

from hash_pk_serializer_base import HashPkSerializerBase

class SysPayRateDefinitionSerializer(HashPkSerializerBase):

    class Meta:
        model = SysPayRateDefinition
