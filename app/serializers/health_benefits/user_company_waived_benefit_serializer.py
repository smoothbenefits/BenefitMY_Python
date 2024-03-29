from rest_framework import serializers 
from app.models.health_benefits.user_company_waived_benefit import \
    UserCompanyWaivedBenefit
from ..company_serializer import CompanySerializer
from ..user_serializer import UserSerializer
from benefit_type_serializer import BenefitTypeSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer


class UserCompanyWaivedBenefitSerializer(HashPkSerializerBase):
    company = CompanySerializer()
    benefit_type = BenefitTypeSerializer()
    user = UserSerializer()
    record_reason = SysBenefitUpdateReasonSerializer()

    class Meta:
        model = UserCompanyWaivedBenefit
