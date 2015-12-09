from rest_framework import serializers
from app.models.insurance.company_group_basic_life_insurance_plan import \
    CompanyGroupBasicLifeInsurancePlan
from app.serializers.insurance.company_life_insurance_plan_serializer import \
    CompanyLifeInsurancePlanSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupBasicLifeInsurancePlanSerializer(HashPkSerializerBase):
    company_basic_life_insurance_plan = CompanyLifeInsurancePlanSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupBasicLifeInsurancePlan


class CompanyGroupBasicLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupBasicLifeInsurancePlan
