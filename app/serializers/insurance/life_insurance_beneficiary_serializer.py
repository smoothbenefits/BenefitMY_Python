from rest_framework import serializers
from app.models.insurance.life_insurance_beneficiary import LifeInsuranceBeneficiary
from hash_pk_serializer_base import HashPkSerializerBase


class LifeInsuranceBeneficiarySerializer(HashPkSerializerBase):
    class Meta:
        model = LifeInsuranceBeneficiary
