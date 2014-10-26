from rest_framework import serializers
from app.models.benefit_plan import BenefitPlan
from benefit_type_serializer import BenefitTypeSerializer


class BenefitPlanSerializer(serializers.ModelSerializer):
    btype = BenefitTypeSerializer()

    class Meta:
        model = BenefitPlan
