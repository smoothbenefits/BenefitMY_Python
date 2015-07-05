from app.models.sys_benefit_update_reason import SysBenefitUpdateReason

from hash_pk_serializer_base import HashPkSerializerBase
from sys_benefit_update_reason_category_serializer import \
    SysBenefitUpdateReasonCategorySerializer


class SysBenefitUpdateReasonSerializer(HashPkSerializerBase):

    category = SysBenefitUpdateReasonCategorySerializer()

    class Meta:
        model = SysBenefitUpdateReason
