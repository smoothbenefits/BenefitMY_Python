from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.commuter.company_commuter_plan import CompanyCommuterPlan
from company_group_commuter_plan_group_only_serializer import \
    CompanyGroupCommuterPlanGroupOnlySerializer


class CompanyCommuterPlanSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")
    company_groups = CompanyGroupCommuterPlanGroupOnlySerializer(
            source="company_group_commuter",
            many=True)

    class Meta:
        model = CompanyCommuterPlan


class CompanyCommuterPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyCommuterPlan
