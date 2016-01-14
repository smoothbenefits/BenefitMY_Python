from rest_framework import serializers
from app.models.health_benefits.benefit_policy_key import BenefitPolicyKey
from ..hash_pk_serializer_base import HashPkSerializerBase


class BenefitPolicyKeySerializer(HashPkSerializerBase):

    class Meta:
        model = BenefitPolicyKey
