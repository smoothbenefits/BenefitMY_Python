from rest_framework import serializers
from app.models.commuter.company_group_commuter_plan import \
    CompanyGroupCommuterPlan
from app.serializers.commuter.company_commuter_plan_serializer import \
    CompanyCommuterPlanSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupCommuterPlanSerializer(HashPkSerializerBase):
    company_commuter_plan = CompanyCommuterPlanSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupCommuterPlan


class CompanyGroupCommuterPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupCommuterPlan
