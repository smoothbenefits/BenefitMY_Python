from rest_framework import serializers
from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan


class CompanyLifeInsurancePlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyLifeInsurancePlan
