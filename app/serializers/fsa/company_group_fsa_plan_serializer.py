from rest_framework import serializers
from app.models.fsa.company_group_fsa_plan import \
    CompanyGroupFsaPlan
from app.serializers.fsa.company_fsa_plan_serializer import \
    CompanyFsaPlanSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupFsaPlanSerializer(HashPkSerializerBase):
    company_fsa_plan = CompanyFsaPlanSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupFsaPlan


class CompanyGroupFsaPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupFsaPlan
