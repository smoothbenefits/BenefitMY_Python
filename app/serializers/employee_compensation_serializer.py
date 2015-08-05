from rest_framework import serializers
from app.models.employee_compensation import EmployeeCompensation
from hash_pk_serializer_base import HashPkSerializerBase
from sys_compensation_update_reason_serializer import SysCompensationUpdateReasonSerializer

class EmployeeCompensationSerializer(HashPkSerializerBase):
    reason = SysCompensationUpdateReasonSerializer()
    class Meta:
        model = EmployeeCompensation

class EmployeeCompensationPostSerializer(HashPkSerializerBase):
    class Meta:
        model = EmployeeCompensation
