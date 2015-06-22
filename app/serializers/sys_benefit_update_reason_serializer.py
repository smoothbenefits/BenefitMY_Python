from app.models.sys_benefit_update_reason import SysBenefitUpdateReason

from hash_pk_serializer_base import HashPkSerializerBase


class SysBenefitUpdateReasonSerializer(HashPkSerializerBase):

    class Meta:
        model = SysBenefitUpdateReason
