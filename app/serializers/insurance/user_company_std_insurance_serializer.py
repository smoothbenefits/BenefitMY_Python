from rest_framework import serializers

from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan

from company_std_insurance_plan_serializer import CompanyStdInsurancePlanSerializer

from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField


class UserCompanyStdInsuranceSerializer(HashPkSerializerBase):
    user = HashField(source="user.id")
    company_std_insurance = CompanyStdInsurancePlanSerializer()

    class Meta:
        model = UserCompanyStdInsurancePlan


class UserCompanyStdInsurancePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompanyStdInsurancePlan
