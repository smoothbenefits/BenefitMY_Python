from rest_framework import serializers
from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan
from hash_pk_serializer_base import HashPkSerializerBase


class CompanyLifeInsurancePlanSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyLifeInsurancePlan
