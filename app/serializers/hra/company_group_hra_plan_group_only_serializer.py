from app.models.hra.company_group_hra_plan import \
    CompanyGroupHraPlan
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupHraPlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupHraPlan
        fields = ('company_group', )
