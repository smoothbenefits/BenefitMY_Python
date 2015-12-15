from rest_framework import serializers
from app.models.insurance.company_group_suppl_life_insurance_plan import \
    CompanyGroupSupplLifeInsurancePlan
from app.serializers.insurance.company_supplemental_life_insurance_plan_serializer import \
    CompanySupplementalLifeInsurancePlanSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupSupplementalLifeInsurancePlanSerializer(HashPkSerializerBase):
    company_suppl_life_insurance_plan = CompanySupplementalLifeInsurancePlanSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupSupplLifeInsurancePlan


class CompanyGroupSupplementalLifeInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupSupplLifeInsurancePlan
