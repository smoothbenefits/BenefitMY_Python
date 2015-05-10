from rest_framework import serializers
from app.models.insurance.comp_suppl_life_insurance_plan import \
    CompSupplLifeInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from supplemental_life_insurance_plan_serializer import (
    SupplementalLifeInsurancePlanSerializer,
    SupplementalLifeInsurancePlanPostSerializer)
from ..custom_fields.hash_field import HashField


class CompanySupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    supplemental_life_insurance_plan = SupplementalLifeInsurancePlanSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompSupplLifeInsurancePlan


class CompanySupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompSupplLifeInsurancePlan
