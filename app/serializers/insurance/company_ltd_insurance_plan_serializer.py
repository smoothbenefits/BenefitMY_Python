from rest_framework import serializers
from app.models.insurance.company_ltd_insurance_plan import \
    CompanyLtdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ltd_insurance_plan_serializer import (
    LtdInsurancePlanSerializer,
    LtdInsurancePlanPostSerializer)
from company_ltd_age_based_rate_serializer import CompanyLtdAgeBasedRateSerializer
from ..custom_fields.hash_field import HashField


class CompanyLtdInsurancePlanSerializer(HashPkSerializerBase):
    ltd_insurance_plan = LtdInsurancePlanSerializer()
    company = HashField(source="company.id")
    age_based_rates = CompanyLtdAgeBasedRateSerializer(many=True)

    class Meta:
        model = CompanyLtdInsurancePlan


class CompanyLtdInsurancePlanPostSerializer(serializers.ModelSerializer):
    age_based_rates = CompanyLtdAgeBasedRateSerializer(many=True, allow_add_remove=True)
    
    class Meta:
        model = CompanyLtdInsurancePlan
