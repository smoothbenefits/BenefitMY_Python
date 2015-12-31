from rest_framework import serializers
from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from life_insurance_plan_serializer import (LifeInsurancePlanSerializer,LifeInsurancePlanPostSerializer)
from company_group_basic_life_insurance_plan_group_only_serializer import \
    CompanyGroupBasicLifeInsurancePlanGroupOnlySerializer
from ..custom_fields.hash_field import HashField


class CompanyLifeInsurancePlanSerializer(HashPkSerializerBase):
    life_insurance_plan = LifeInsurancePlanSerializer()
    company = HashField(source="company.id")
    company_groups = CompanyGroupBasicLifeInsurancePlanGroupOnlySerializer(
        source="company_group_basic_life_insurance", 
        many=True)

    class Meta:
        model = CompanyLifeInsurancePlan


class CompanyLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyLifeInsurancePlan
