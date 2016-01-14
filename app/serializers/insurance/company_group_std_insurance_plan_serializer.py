from rest_framework import serializers
from app.models.insurance.company_group_std_insurance_plan import \
    CompanyGroupStdInsurancePlan
from app.serializers.insurance.company_std_insurance_plan_serializer import \
    CompanyStdInsurancePlanSerializer
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupStdInsurancePlanSerializer(HashPkSerializerBase):
    company_std_insurance_plan = CompanyStdInsurancePlanSerializer()
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupStdInsurancePlan


class CompanyGroupStdInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyGroupStdInsurancePlan
