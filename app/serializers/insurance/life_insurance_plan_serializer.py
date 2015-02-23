from rest_framework import serializers
from app.models.insurance.life_insurance_plan import LifeInsurancePlan
from hash_pk_serializer_base import HashPkSerializerBase


class LifeInsurancePlanSerializer(HashPkSerializerBase):
    class Meta:
        model = LifeInsurancePlan

