from app.models.sys_benefit_update_reason_category import SysBenefitUpdateReasonCategory

from hash_pk_serializer_base import HashPkSerializerBase

class SysBenefitUpdateReasonCategorySerializer(HashPkSerializerBase):

    class Meta:
        model = SysBenefitUpdateReasonCategory
