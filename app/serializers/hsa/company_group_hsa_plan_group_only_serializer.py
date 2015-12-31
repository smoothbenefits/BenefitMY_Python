from app.models.hsa.company_group_hsa_plan import CompanyGroupHsaPlan
from app.serializers.company_group_serializer import CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase

class CompanyGroupHsaPlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupHsaPlan
        fields = ('company_group', )
