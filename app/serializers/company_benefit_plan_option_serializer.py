from rest_framework import serializers
from app.models.company_benefit_plan_option import CompanyBenefitPlanOption

from company_serializer import CompanySerializer
from benefit_plan_serializer import BenefitPlanSerializer


class CompanyBenefitPlanOptionSerializer(serializers.ModelSerializer):

    company = CompanySerializer()
    benefit_plan = BenefitPlanSerializer()

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'company',
                  'benefit_plan')


class CompanyBenefitPlanSerializer(serializers.ModelSerializer):

    benefit_plan = BenefitPlanSerializer()

    class Meta:

        model = CompanyBenefitPlanOption
        fields = ('id',
                  'total_cost_per_period',
                  'employee_cost_per_period',
                  'benefit_option_type',
                  'benefit_plan')


