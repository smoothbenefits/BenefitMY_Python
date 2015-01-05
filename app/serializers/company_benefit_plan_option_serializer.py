from rest_framework import serializers
from app.models.company_benefit_plan_option import CompanyBenefitPlanOption

from benefit_plan_serializer import (
    BenefitPlanSerializer,
    BenefitPlanPostSerializer)


class CompanyBenefitPlanOptionPostSerializer(serializers.ModelSerializer):

    benefit_plan = BenefitPlanPostSerializer()

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'company',
                  'benefit_plan',
                  'pcp_link')


class CompanyBenefitPlanOptionSerializer(serializers.ModelSerializer):

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'company',
                  'benefit_plan',
                  'pcp_link')
        depth = 2


class CompanyBenefitPlanSerializer(serializers.ModelSerializer):

    benefit_plan = BenefitPlanSerializer()

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'benefit_plan',
                  'pcp_link')
