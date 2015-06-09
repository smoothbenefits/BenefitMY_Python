from rest_framework import serializers

from app.models.user_company_benefit_plan_option import \
    UserCompanyBenefitPlanOption

from app.serializers.enrolled_serializer import EnrolledSerializer
from company_benefit_plan_option_serializer import CompanyBenefitPlanOptionSerializer
from hash_pk_serializer_base import HashPkSerializerBase


class UserCompanyBenefitPlanOptionSerializer(HashPkSerializerBase):
    enrolleds = EnrolledSerializer(many=True)
    benefit = CompanyBenefitPlanOptionSerializer()

    class Meta:

        model = UserCompanyBenefitPlanOption
        fields = ('enrolleds', 'benefit', 'created_at', 'updated_at')
