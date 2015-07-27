from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.insurance.supplemental_life_insurance_beneficiary import \
    SupplementalLifeInsuranceBeneficiary


class SupplementalLifeInsuranceBeneficiarySerializer(HashPkSerializerBase):

    person_comp_suppl_life_insurance_plan = HashField(source="person_comp_suppl_life_insurance_plan.id")

    class Meta:
        model = SupplementalLifeInsuranceBeneficiary


class SupplementalLifeInsuranceBeneficiaryPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplementalLifeInsuranceBeneficiary
