from rest_framework import serializers

from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption

from app.serializers.company_benefit_plan_option_serializer import \
    CompanyBenefitPlanOptionSerializer
from app.serializers.enrolled_serializer import EnrolledSerializer


class UserCompanyBenefitPlanOptionSerializer(serializers.ModelSerializer):
    company_benefit_plan_option = CompanyBenefitPlanOptionSerializer()
    enrolled = EnrolledSerializer(many=True)

    class Meta:

        model = UserCompanyBenefitPlanOption
