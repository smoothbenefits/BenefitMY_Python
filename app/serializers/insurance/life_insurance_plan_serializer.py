from rest_framework import serializers
from app.models.insurance.life_insurance_plan import LifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class LifeInsurancePlanSerializer(HashPkSerializerBase):

    user = HashField(source="user.id")

    class Meta:
        model = LifeInsurancePlan

class LifeInsurancePlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = LifeInsurancePlan

