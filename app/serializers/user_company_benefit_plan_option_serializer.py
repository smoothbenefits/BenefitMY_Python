from rest_framework import serializers

from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption

from app.serializers.enrolled_serializer import EnrolledSerializer


class UserCompanyBenefitPlanOptionSerializer(serializers.ModelSerializer):
    enrolleds = EnrolledSerializer(many=True)

    class Meta:

        model = UserCompanyBenefitPlanOption
        fields = ('enrolleds', 'benefit', 'waived_benefit')
        depth = 2


class UserBenefitPostSerializer(serializers.ModelSerializer):
    enrolled = serializers.SlugRelatedField(many=True, slug_field='id')
    #waived_benefit = UserCompanyWaivedBenefitSerializer()
    #benefit = serializers.SlugRelatedField(slug_filed='id')

    class Meta:

        model = UserCompanyBenefitPlanOption
        fields = ("user", "benefit", "enrolled", "waived_benefit")
