from rest_framework import serializers
from app.models.insurance.company_ltd_insurance_plan import \
    CompanyLtdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ltd_insurance_plan_serializer import (
    LtdInsurancePlanSerializer,
    LtdInsurancePlanPostSerializer)
from ..custom_fields.hash_field import HashField


class CompanyLtdInsurancePlanSerializer(HashPkSerializerBase):
    ltd_insurance_plan = LtdInsurancePlanSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanyLtdInsurancePlan


class CompanyLtdInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyLtdInsurancePlan
