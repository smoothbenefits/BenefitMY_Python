from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.insurance.supplemental_life_insurance_plan import SupplementalLifeInsurancePlan
from supplemental_life_insurance_plan_rate_serializer import (
    SupplementalLifeInsurancePlanRateSerializer,
    SupplementalLifeInsurancePlanRatePostSerializer)

class SupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    supplemental_life_insurance_plan_rate = SupplementalLifeInsurancePlanRateSerializer()

    class Meta:
        model = SupplementalLifeInsurancePlan


class SupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):
    supplemental_life_insurance_plan_rate = SupplementalLifeInsurancePlanRatePostSerializer()
    
    class Meta:
        model = SupplementalLifeInsurancePlan
