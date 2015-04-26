from rest_framework import serializers
from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from std_insurance_plan_serializer import (
    StdInsurancePlanSerializer,
    StdInsurancePlanPostSerializer)
from ..custom_fields.hash_field import HashField


class CompanyStdInsurancePlanSerializer(HashPkSerializerBase):
    std_insurance_plan = StdInsurancePlanSerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanyStdInsurancePlan


class CompanyStdInsurancePlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyStdInsurancePlan
