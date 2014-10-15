from rest_framework import serializers
from app.models.benefit_type import BenefitType


class BenefitTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BenefitType

