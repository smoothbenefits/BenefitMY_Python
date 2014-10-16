from rest_framework import serializers
from app.models.benefit_plan import BenefitPlan


class BenefitPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = BenefitPlan

