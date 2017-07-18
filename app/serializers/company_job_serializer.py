from rest_framework import serializers
from custom_fields.hash_field import HashField
from hash_pk_serializer_base import HashPkSerializerBase

from app.models.company_job import CompanyJob


class CompanyJobSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyJob


class CompanyJobPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyJob
