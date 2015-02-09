from rest_framework import serializers
from app.models.benefit_plan import BenefitPlan
from benefit_type_serializer import BenefitTypeSerializer
from hash_pk_serializer_base import HashPkSerializerBase


class BenefitPlanSerializer(HashPkSerializerBase):
    benefit_type = BenefitTypeSerializer()

    class Meta:
        model = BenefitPlan


class BenefitPlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = BenefitPlan
