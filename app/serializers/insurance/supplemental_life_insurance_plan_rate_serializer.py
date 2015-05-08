from rest_framework import serializers
from app.models.insurance.supplemental_life_insurance_plan_rate import SupplementalLifeInsurancePlanRate
from supplemental_life_insurance_plan_serializer import SupplementalLifeInsurancePlanSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class SupplementalLifeInsurancePlanRateSerializer(HashPkSerializerBase):

	supplemental_life_insurance_plan = SupplementalLifeInsurancePlanSerializer

    class Meta:
        model = SupplementalLifeInsurancePlanRate


class StdInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplementalLifeInsurancePlanRate
