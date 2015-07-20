from rest_framework import serializers
from app.models.benefit_type import BenefitType
from hash_pk_serializer_base import HashPkSerializerBase


class BenefitTypeSerializer(HashPkSerializerBase):

    class Meta:
        model = BenefitType
