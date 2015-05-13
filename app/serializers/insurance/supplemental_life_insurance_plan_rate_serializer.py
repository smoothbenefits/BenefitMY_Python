from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..sys_suppl_life_insurance_condition_serializer import SysSupplLifeInsuranceConditionSerializer
from app.models.insurance.supplemental_life_insurance_plan_rate import SupplementalLifeInsurancePlanRate

class SupplementalLifeInsurancePlanRateSerializer(HashPkSerializerBase):

    condition = SysSupplLifeInsuranceConditionSerializer()
    supplemental_life_insurance_plan = HashField(source="supplemental_life_insurance_plan.id")

    class Meta:
        model = SupplementalLifeInsurancePlanRate


class SupplementalLifeInsurancePlanRatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplementalLifeInsurancePlanRate
