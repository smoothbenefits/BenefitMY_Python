from rest_framework import serializers
from app.models.benefit_details import BenefitDetails

class BenefitDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BenefitDetails
        depth = 1
