from rest_framework import serializers
from custom_fields.hash_field import HashField
from hash_pk_serializer_base import HashPkSerializerBase

from app.models.company_department import CompanyDepartment


class CompanyDepartmentSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyDepartment


class CompanyDepartmentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDepartment
