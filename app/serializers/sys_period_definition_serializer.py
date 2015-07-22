from app.models.sys_period_definition import SysPeriodDefinition

from hash_pk_serializer_base import HashPkSerializerBase


class SysPeriodDefinitionSerializer(HashPkSerializerBase):

    class Meta:
        model = SysPeriodDefinition