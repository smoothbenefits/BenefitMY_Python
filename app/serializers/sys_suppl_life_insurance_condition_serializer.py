from hash_pk_serializer_base import HashPkSerializerBase
from app.models.sys_suppl_life_insurance_condition import SysSupplLifeInsuranceCondition

class SysApplicationFeatureSerializer(HashPkSerializerBase):

    class Meta:
        model = SysSupplLifeInsuranceCondition
