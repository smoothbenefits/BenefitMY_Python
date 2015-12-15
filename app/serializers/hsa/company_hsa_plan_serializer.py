from rest_framework import serializers
from app.models.hsa.company_hsa_plan import CompanyHsaPlan
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase

class CompanyHsaPlanSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyHsaPlan

class CompanyHsaPlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyHsaPlan
