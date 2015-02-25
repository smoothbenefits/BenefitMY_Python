from rest_framework import serializers
from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from life_insurance_plan_serializer import (LifeInsurancePlanSerializer,LifeInsurancePlanPostSerializer)
from ..custom_fields.hash_field import HashField


class CompanyLifeInsurancePlanSerializer(HashPkSerializerBase):
    life_insurance_plan = LifeInsurancePlanSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanyLifeInsurancePlan


class CompanyLifeInsurancePlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyLifeInsurancePlan
