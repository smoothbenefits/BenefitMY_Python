from rest_framework import serializers
from app.models.employee_profile import EmployeeProfile
from app.models.person import Person
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from sys_period_definition_serializer import SysPeriodDefinitionSerializer


class ManagerSerializer(HashPkSerializerBase):
    first_name = serializers.CharField(source="person.first_name", required=False)
    last_name = serializers.CharField(source="person.last_name", required=False)
    person = HashField(source="person.id")
    class Meta:
        model = EmployeeProfile
        fields = ('id', 'first_name', 'last_name', 'person')


class EmployeeProfileSerializer(HashPkSerializerBase):
    person = HashField(source="person.id")
    company = HashField(source="company.id")
    pay_rate = SysPeriodDefinitionSerializer()
    manager = ManagerSerializer(required=False)
    class Meta:
        model = EmployeeProfile


class EmployeeProfilePostSerializer(HashPkSerializerBase):
    class Meta:
        model = EmployeeProfile


class EmployeeProfileWithNameSerializer(HashPkSerializerBase):
    first_name = serializers.CharField(source="person.first_name", required=False)
    last_name = serializers.CharField(source="person.last_name", required=False)
    manager = ManagerSerializer(required=False)
    class Meta:
        model = EmployeeProfile
