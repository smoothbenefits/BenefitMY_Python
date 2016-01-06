from app.models.fsa.company_group_fsa_plan import \
    CompanyGroupFsaPlan
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupFsaPlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupFsaPlan
        fields = ('company_group', )
