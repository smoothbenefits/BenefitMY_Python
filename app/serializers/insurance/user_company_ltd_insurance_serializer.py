from rest_framework import serializers

from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan

from company_ltd_insurance_plan_serializer import CompanyLtdInsurancePlanSerializer

from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField
from ..sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer


class UserCompanyLtdInsuranceSerializer(HashPkSerializerBase):
    user = HashField(source="user.id")
    company_ltd_insurance = CompanyLtdInsurancePlanSerializer()
    record_reason = SysBenefitUpdateReasonSerializer()

    class Meta:
        model = UserCompanyLtdInsurancePlan


class UserCompanyLtdInsurancePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompanyLtdInsurancePlan
