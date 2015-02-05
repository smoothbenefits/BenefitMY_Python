from rest_framework import serializers
from app.models.life_insurance_plan import LifeInsurancePlan


class LifeInsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeInsurancePlan

