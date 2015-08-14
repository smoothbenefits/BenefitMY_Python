from rest_framework import serializers
from app.models.employee_profile import EmployeeProfile
from app.models.person import Person
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from sys_pay_rate_definition_serializer import SysPayRateDefinitionSerializer

class EmployeeProfileSerializer(HashPkSerializerBase):
    person = HashField(source="person.id")
    company = HashField(source="company.id")
    pay_rate = SysPayRateDefinitionSerializer()
    class Meta:
        model = EmployeeProfile

class EmployeeProfilePostSerializer(HashPkSerializerBase):
    class Meta:
        model = EmployeeProfile
