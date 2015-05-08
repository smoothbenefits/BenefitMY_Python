from rest_framework import serializers
from app.models.insurance.company_supplemental_life_insurance_plan import \
    CompanySupplementalLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from supplemental_life_insurance_plan_serializer import (
    SupplementalLifeInsurancePlanSerializer,
    SupplementalLifeInsurancePlanPostSerializer)
from ..custom_fields.hash_field import HashField


class CompanySupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    supplemental_life_insurance_plan = SupplementalLifeInsurancePlanSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanySupplementalLifeInsurancePlan


class CompanySupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanySupplementalLifeInsurancePlan
