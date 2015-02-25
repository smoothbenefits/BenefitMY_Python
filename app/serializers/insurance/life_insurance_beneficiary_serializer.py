from rest_framework import serializers
from app.models.insurance.life_insurance_beneficiary import LifeInsuranceBeneficiary
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField


class LifeInsuranceBeneficiarySerializer(HashPkSerializerBase):

    user_life_insurance_plan = HashField(source="user_life_insurance_plan.id")

    class Meta:
        model = LifeInsuranceBeneficiary


class LifeInsuranceBeneficiaryPostSerializer(HashPkSerializerBase):
    
    class Meta:
        model = LifeInsuranceBeneficiary