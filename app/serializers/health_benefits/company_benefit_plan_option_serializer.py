from rest_framework import serializers
from app.models.health_benefits.company_benefit_plan_option import CompanyBenefitPlanOption

from benefit_plan_serializer import (
    BenefitPlanSerializer,
    BenefitPlanPostSerializer)
from company_group_benefit_plan_option_group_only_serializer import \
    CompanyGroupBenefitPlanOptionGroupOnlySerializer
from ..company_serializer import ShallowCompanySerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyBenefitPlanOptionPostSerializer(HashPkSerializerBase):

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'company',
                  'benefit_plan')


class CompanyBenefitPlanOptionSerializer(HashPkSerializerBase):

    company = ShallowCompanySerializer()
    benefit_plan = BenefitPlanSerializer()
    company_groups = CompanyGroupBenefitPlanOptionGroupOnlySerializer(
        source="company_group_benefit_plan_option",
        many=True)

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'company',
                  'benefit_plan')


class CompanyBenefitPlanSerializer(HashPkSerializerBase):

    benefit_plan = BenefitPlanSerializer()

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'benefit_plan')
