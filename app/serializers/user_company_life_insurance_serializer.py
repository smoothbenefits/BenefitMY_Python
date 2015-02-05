from rest_framework import serializers

from app.models.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan

from app.serializers.life_insurance_enrolled_serializer import \
    LifeInsuranceEnrolledSerializer


class UserCompanyLifeInsuranceSerializer(serializers.ModelSerializer):
    life_insurance_enrolleds = LifeInsuranceEnrolledSerializer(many=True)

    class Meta:
        model = UserCompanyLifeInsurancePlan
