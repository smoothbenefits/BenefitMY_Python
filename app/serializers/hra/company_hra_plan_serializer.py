from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.hra.company_hra_plan import CompanyHraPlan
from hra_plan_serializer import HraPlanSerializer
from company_group_hra_plan_group_only_serializer import \
    CompanyGroupHraPlanGroupOnlySerializer


class CompanyHraPlanSerializer(HashPkSerializerBase):
    hra_plan = HraPlanSerializer()
    company = HashField(source="company.id")
    company_groups = CompanyGroupHraPlanGroupOnlySerializer(
            source="company_group_hra",
            many=True)

    class Meta:
        model = CompanyHraPlan


class CompanyHraPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyHraPlan
