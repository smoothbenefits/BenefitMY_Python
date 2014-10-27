from rest_framework import serializers

from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption

from app.serializers.company_benefit_plan_option_serializer import \
    CompanyBenefitPlanOptionSerializer
from app.serializers.enrolled_serializer import EnrolledSerializer
from app.serializers.user_company_waived_benefit_serializer import \
    UserCompanyWaivedBenefitSerializer


class UserCompanyBenefitPlanOptionSerializer(serializers.ModelSerializer):
    company_benefit_plan_option = CompanyBenefitPlanOptionSerializer()
    enrolled = EnrolledSerializer(many=True)
    waived_benefit = UserCompanyWaivedBenefitSerializer()

    class Meta:

        model = UserCompanyBenefitPlanOption


class UserBenefitPostSerializer(serializers.ModelSerializer):
    enrolled = serializers.SlugRelatedField(many=True, slug_field='id')
    #waived_benefit = UserCompanyWaivedBenefitSerializer()
    #benefit = serializers.SlugRelatedField(slug_filed='id')

    class Meta:

        model = UserCompanyBenefitPlanOption
        fields = ("user", "company_benefit_plan_option", "enrolled")
