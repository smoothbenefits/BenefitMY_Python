from rest_framework import serializers
from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from fsa_plan_serializer import FsaPlanSerializer
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from company_group_fsa_plan_group_only_serializer import \
    CompanyGroupFsaPlanGroupOnlySerializer

class CompanyFsaPlanSerializer(HashPkSerializerBase):
    fsa_plan = FsaPlanSerializer()
    company = HashField(source="company.id")
    company_groups = CompanyGroupFsaPlanGroupOnlySerializer(
            source="company_group_fsa",
            many=True)

    class Meta:
        model = CompanyFsaPlan

class CompanyFsaPlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyFsaPlan
