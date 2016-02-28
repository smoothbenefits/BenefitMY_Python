from rest_framework import serializers
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField
from app.models.company_service_provider import CompanyServiceProvider


class CompanyServiceProviderSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyServiceProvider


class CompanyServiceProviderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyServiceProvider
