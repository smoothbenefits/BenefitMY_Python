from rest_framework import serializers
from app.models.hsa.company_group_hsa_plan import CompanyGroupHsaPlan
from app.serializers.company_group_serializer import CompanyGroupSerializer
from company_hsa_plan_serializer import CompanyHsaPlanSerializer
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase

class CompanyGroupHsaPlanSerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()
    company_hsa_plan = CompanyHsaPlanSerializer()

    class Meta:
        model = CompanyGroupHsaPlan

class CompanyGroupHsaPlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyGroupHsaPlan
