from rest_framework import serializers

from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan

from life_insurance_beneficiary_serializer import \
    LifeInsuranceBeneficiarySerializer


class UserCompanyLifeInsuranceSerializer(serializers.ModelSerializer):
    life_insurance_beneficiary = LifeInsuranceBeneficiarySerializer(many=True)

    class Meta:
        model = UserCompanyLifeInsurancePlan
