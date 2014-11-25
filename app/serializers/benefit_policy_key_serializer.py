from rest_framework import serializers
from app.models.benefit_policy_key import BenefitPolicyKey


class BenefitPolicyKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = BenefitPolicyKey

