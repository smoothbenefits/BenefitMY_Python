from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..sys_suppl_life_insurance_condition_serializer import SysApplicationFeatureSerializer
from app.models.insurance.supplemental_life_insurance_plan_rate import SupplementalLifeInsurancePlanRate
from supplemental_life_insurance_plan_serializer import SupplementalLifeInsurancePlanSerializer

class SupplementalLifeInsurancePlanRateSerializer(HashPkSerializerBase):

    supplemental_life_insurance_plan = SupplementalLifeInsurancePlanSerializer()
    condition_key = SysApplicationFeatureSerializer()

    class Meta:
        model = SupplementalLifeInsurancePlanRate


class SupplementalLifeInsurancePlanRatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplementalLifeInsurancePlanRate
