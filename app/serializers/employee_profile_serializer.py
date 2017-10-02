from rest_framework import serializers
from app.models.employee_profile import EmployeeProfile
from app.models.person import Person
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from sys_period_definition_serializer import SysPeriodDefinitionSerializer
from app.serializers.person_serializer import PersonSerializer
from app.serializers.company_department_serializer import CompanyDepartmentSerializer
from app.serializers.company_job_serializer import CompanyJobSerializer
from app.serializers.company_division_serializer import CompanyDivisionSerializer


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
    department = CompanyDepartmentSerializer(required=False)
    job = CompanyJobSerializer(required=False)
    division = CompanyDivisionSerializer(required=False)
    class Meta:
        model = EmployeeProfile


class EmployeeProfilePostSerializer(HashPkSerializerBase):
    department = CompanyDepartmentSerializer(required=False)
    division = CompanyDivisionSerializer(required=False)
    job = CompanyJobSerializer(required=False)
    class Meta:
        model = EmployeeProfile


class EmployeeProfileWithNameSerializer(HashPkSerializerBase):
    first_name = serializers.CharField(source="person.first_name", required=False)
    last_name = serializers.CharField(source="person.last_name", required=False)
    manager = ManagerSerializer(required=False)
    person = PersonSerializer()
    department = CompanyDepartmentSerializer(required=False)
    job = CompanyJobSerializer(required=False)
    division = CompanyDivisionSerializer(required=False)
    class Meta:
        model = EmployeeProfile
