from rest_framework import serializers
from app.models.benefit_policy_type import BenefitPolicyType


class BenefitPolicyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BenefitPolicyType

