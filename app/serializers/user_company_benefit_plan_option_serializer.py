from rest_framework import serializers

from app.models.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption

from app.serializers.enrolled_serializer import EnrolledSerializer


class UserCompanyBenefitPlanOptionSerializer(serializers.ModelSerializer):
    enrolleds = EnrolledSerializer(many=True)

    class Meta:

        model = UserCompanyBenefitPlanOption
        fields = ('enrolleds', 'benefit', 'pcp', 'created_at', 'updated_at')
        depth = 2
