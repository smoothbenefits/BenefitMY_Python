from rest_framework import serializers
from app.models.insurance.ltd_insurance_plan import LtdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class LtdInsurancePlanSerializer(HashPkSerializerBase):

    user = HashField(source="user.id")

    class Meta:
        model = LtdInsurancePlan


class LtdInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LtdInsurancePlan
