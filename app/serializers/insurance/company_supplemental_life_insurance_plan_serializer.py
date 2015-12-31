from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.insurance.comp_suppl_life_insurance_plan import \
    CompSupplLifeInsurancePlan
from supplemental_life_insurance_plan_serializer import (
    SupplementalLifeInsurancePlanSerializer,
    SupplementalLifeInsurancePlanPostSerializer)
from company_group_supplemental_life_insurance_plan_group_only_serializer import \
    CompanyGroupSupplementalLifeInsurancePlanGroupOnlySerializer


class CompanySupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    supplemental_life_insurance_plan = SupplementalLifeInsurancePlanSerializer()
    company = HashField(source="company.id")
    company_groups = CompanyGroupSupplementalLifeInsurancePlanGroupOnlySerializer(
        source="company_group_suppl_life_insurance",
        many=True)

    class Meta:
        model = CompSupplLifeInsurancePlan


class CompanySupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompSupplLifeInsurancePlan
