from rest_framework import serializers
from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from std_insurance_plan_serializer import (
    StdInsurancePlanSerializer,
    StdInsurancePlanPostSerializer)
from company_std_age_based_rate_serializer import CompanyStdAgeBasedRateSerializer, CompanyStdAgeBasedRatePostSerializer
from ..custom_fields.hash_field import HashField


class CompanyStdInsurancePlanSerializer(HashPkSerializerBase):
    std_insurance_plan = StdInsurancePlanSerializer()
    age_based_rates = CompanyStdAgeBasedRateSerializer(many=True)
    company = HashField(source="company.id")

    class Meta:
        model = CompanyStdInsurancePlan
        fields = ('elimination_period_in_days',
                  'duration',
                  'percentage_of_salary',
                  'max_benefit_weekly',
                  'rate',
                  'age_based_rates',
                  'employer_contribution_percentage',
                  'paid_by',
                  'company',
                  'std_insurance_plan',
                  'created_at',
                  'updated_at')


class CompanyStdInsurancePlanPostSerializer(HashPkSerializerBase):
    age_based_rates = CompanyStdAgeBasedRatePostSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = CompanyStdInsurancePlan
        fields = ('elimination_period_in_days',
                  'duration',
                  'percentage_of_salary',
                  'max_benefit_weekly',
                  'rate',
                  'age_based_rates',
                  'employer_contribution_percentage',
                  'paid_by',
                  'company',
                  'std_insurance_plan',
                  'created_at',
                  'updated_at')
