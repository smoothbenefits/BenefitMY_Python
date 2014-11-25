from rest_framework import serializers
from app.models.benefit_key import BenefitKey


class BenefitKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = BenefitKey

