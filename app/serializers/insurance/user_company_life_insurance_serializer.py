from rest_framework import serializers

from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan

from life_insurance_beneficiary_serializer import \
    LifeInsuranceBeneficiarySerializer

from hash_pk_serializer_base import HashPkSerializerBase


class UserCompanyLifeInsuranceSerializer(HashPkSerializerBase):
    life_insurance_beneficiary = LifeInsuranceBeneficiarySerializer(many=True)

    class Meta:
        model = UserCompanyLifeInsurancePlan
