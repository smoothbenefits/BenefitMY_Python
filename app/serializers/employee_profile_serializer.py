from rest_framework import serializers
from app.models.employee_profile import EmployeeProfile
from app.models.person import Person
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from sys_period_definition_serializer import SysPeriodDefinitionSerializer

class EmployeeProfileSerializer(HashPkSerializerBase):
    person = HashField(source="person.id")
    company = HashField(source="company.id")
    pay_rate = SysPeriodDefinitionSerializer()
    class Meta:
        model = EmployeeProfile

class EmployeeProfilePostSerializer(HashPkSerializerBase):
    class Meta:
        model = EmployeeProfile
