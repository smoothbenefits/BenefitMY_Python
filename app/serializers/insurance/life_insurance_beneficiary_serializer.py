from rest_framework import serializers
from app.models.insurance.life_insurance_beneficiary import LifeInsuranceBeneficiary


class LifeInsuranceBeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeInsuranceBeneficiary
