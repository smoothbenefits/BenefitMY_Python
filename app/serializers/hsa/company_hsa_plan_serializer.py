from rest_framework import serializers
from app.models.hsa.company_hsa_plan import CompanyHsaPlan
from company_group_hsa_plan_group_only_serializer import \
    CompanyGroupHsaPlanGroupOnlySerializer
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase

class CompanyHsaPlanSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")
    company_groups = CompanyGroupHsaPlanGroupOnlySerializer(
        source="company_group_hsa_plan", many=True)

    class Meta:
        model = CompanyHsaPlan

class CompanyHsaPlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyHsaPlan
