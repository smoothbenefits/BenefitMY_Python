from rest_framework import serializers
from app.models.hra.company_group_hra_plan import \
    CompanyGroupHraPlan
from app.serializers.hra.company_hra_plan_serializer import \
    CompanyHraPlanSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupHraPlanSerializer(HashPkSerializerBase):
    company_hra_plan = CompanyHraPlanSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupHraPlan


class CompanyGroupHraPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupHraPlan
