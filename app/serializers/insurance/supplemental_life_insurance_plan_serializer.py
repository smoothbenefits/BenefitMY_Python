from rest_framework import serializers
from app.models.insurance.supplemental_life_insurance_plan import SupplementalLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class SupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):

    class Meta:
        model = SupplementalLifeInsurancePlan


class SupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplementalLifeInsurancePlan
