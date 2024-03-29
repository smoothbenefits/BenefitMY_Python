from rest_framework import serializers
from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from std_insurance_plan_serializer import (
    StdInsurancePlanSerializer,
    StdInsurancePlanPostSerializer)
from company_group_std_insurance_plan_group_only_serializer import CompanyGroupStdInsurancePlanGroupOnlySerializer
from company_std_age_based_rate_serializer import CompanyStdAgeBasedRateSerializer, CompanyStdAgeBasedRatePostSerializer
from ..custom_fields.hash_field import HashField


class CompanyStdInsurancePlanSerializer(HashPkSerializerBase):
    std_insurance_plan = StdInsurancePlanSerializer()
    age_based_rates = CompanyStdAgeBasedRateSerializer(many=True)
    company = HashField(source="company.id")
    company_groups = CompanyGroupStdInsurancePlanGroupOnlySerializer(
        source='company_group_std', many=True)

    class Meta:
        model = CompanyStdInsurancePlan
        fields = ('id',
                  'company_groups',
                  'elimination_period_in_days',
                  'duration',
                  'percentage_of_salary',
                  'max_benefit_weekly',
                  'rate',
                  'user_amount_required',
                  'benefit_amount_step',
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
        fields = ('id',
                  'elimination_period_in_days',
                  'duration',
                  'percentage_of_salary',
                  'max_benefit_weekly',
                  'rate',
                  'user_amount_required',
                  'benefit_amount_step',
                  'age_based_rates',
                  'employer_contribution_percentage',
                  'paid_by',
                  'company',
                  'std_insurance_plan',
                  'created_at',
                  'updated_at')
