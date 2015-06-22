from rest_framework import serializers

from app.models.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption

from app.serializers.enrolled_serializer import EnrolledSerializer
from company_benefit_plan_option_serializer import CompanyBenefitPlanOptionSerializer
from hash_pk_serializer_base import HashPkSerializerBase
from sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer


class UserCompanyBenefitPlanOptionSerializer(HashPkSerializerBase):
    enrolleds = EnrolledSerializer(many=True)
    benefit = CompanyBenefitPlanOptionSerializer()
    record_reason = SysBenefitUpdateReasonSerializer()

    class Meta:

        model = UserCompanyBenefitPlanOption
        fields = ('enrolleds', 'benefit', 'record_reason', 'created_at', 'updated_at')
