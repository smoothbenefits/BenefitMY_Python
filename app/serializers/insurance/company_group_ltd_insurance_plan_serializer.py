from rest_framework import serializers
from app.models.insurance.company_group_ltd_insurance_plan import \
    CompanyGroupLtdInsurancePlan
from app.serializers.insurance.company_ltd_insurance_plan_serializer import \
    CompanyLtdInsurancePlanSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupLtdInsurancePlanSerializer(HashPkSerializerBase):
    company_ltd_insurance_plan = CompanyLtdInsurancePlanSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupLtdInsurancePlan


class CompanyGroupLtdInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupLtdInsurancePlan
