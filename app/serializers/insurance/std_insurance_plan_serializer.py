from rest_framework import serializers
from app.models.insurance.std_insurance_plan import StdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class StdInsurancePlanSerializer(HashPkSerializerBase):

    user = HashField(source="user.id")

    class Meta:
        model = StdInsurancePlan


class StdInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = StdInsurancePlan
