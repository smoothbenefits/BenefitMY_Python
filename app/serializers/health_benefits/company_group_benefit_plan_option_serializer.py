from rest_framework import serializers
from app.models.health_benefits.company_group_benefit_plan_option import \
    CompanyGroupBenefitPlanOption
from app.serializers.health_benefits.company_benefit_plan_option_serializer import \
    CompanyBenefitPlanOptionSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupBenefitPlanOptionSerializer(HashPkSerializerBase):
    company_benefit_plan_option = CompanyBenefitPlanOptionSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupBenefitPlanOption


class CompanyGroupBenefitPlanOptionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupBenefitPlanOption
