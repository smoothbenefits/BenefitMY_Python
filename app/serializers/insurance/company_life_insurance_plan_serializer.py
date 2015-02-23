from rest_framework import serializers
from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from life_insurance_plan_serializer import LifeInsurancePlanSerializer


class CompanyLifeInsurancePlanSerializer(HashPkSerializerBase):
    life_insurance_plan = LifeInsurancePlanSerializer()
    class Meta:
        model = CompanyLifeInsurancePlan
