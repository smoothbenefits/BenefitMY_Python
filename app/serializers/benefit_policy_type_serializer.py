from rest_framework import serializers
from app.models.benefit_policy_type import BenefitPolicyType
from hash_pk_serializer_base import HashPkSerializerBase


class BenefitPolicyTypeSerializer(HashPkSerializerBase):

    class Meta:
        model = BenefitPolicyType

