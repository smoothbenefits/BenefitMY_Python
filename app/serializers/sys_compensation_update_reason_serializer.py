from rest_framework import serializers
from app.models.sys_compensation_update_reason import SysCompensationUpdateReason
from hash_pk_serializer_base import HashPkSerializerBase

class SysCompensationUpdateReasonSerializer(HashPkSerializerBase):

    class Meta:
        model = SysCompensationUpdateReason
