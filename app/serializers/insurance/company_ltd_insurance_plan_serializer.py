from rest_framework import serializers
from app.models.insurance.company_ltd_insurance_plan import \
    CompanyLtdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ltd_insurance_plan_serializer import (
    LtdInsurancePlanSerializer,
    LtdInsurancePlanPostSerializer)
from company_ltd_age_based_rate_serializer import CompanyLtdAgeBasedRateSerializer, CompanyLtdAgeBasedRatePostSerializer
from ..custom_fields.hash_field import HashField


class CompanyLtdInsurancePlanSerializer(HashPkSerializerBase):
    ltd_insurance_plan = LtdInsurancePlanSerializer()
    company = HashField(source="company.id")
    age_based_rates = CompanyLtdAgeBasedRateSerializer(many=True)

    class Meta:
        model = CompanyLtdInsurancePlan
        fields = ('id',
                  'elimination_period_in_months',
                  'duration',
                  'percentage_of_salary',
                  'max_benefit_monthly',
                  'rate',
                  'age_based_rates',
                  'employer_contribution_percentage',
                  'paid_by',
                  'company',
                  'ltd_insurance_plan',
                  'created_at',
                  'updated_at')


class CompanyLtdInsurancePlanPostSerializer(HashPkSerializerBase):
    age_based_rates = CompanyLtdAgeBasedRatePostSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = CompanyLtdInsurancePlan
        fields = ('id',
                  'elimination_period_in_months',
                  'duration',
                  'percentage_of_salary',
                  'max_benefit_monthly',
                  'rate',
                  'age_based_rates',
                  'employer_contribution_percentage',
                  'paid_by',
                  'company',
                  'ltd_insurance_plan',
                  'created_at',
                  'updated_at')
