from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.extra_benefits.extra_benefit_item import \
    ExtraBenefitItem


class ExtraBenefitItemSerializer(HashPkSerializerBase):
    company_plan = HashField(source="company_plan.id")

    class Meta:
        model = ExtraBenefitItem


class ExtraBenefitItemPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtraBenefitItem
