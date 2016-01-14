from app.models.commuter.company_group_commuter_plan import \
    CompanyGroupCommuterPlan
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupCommuterPlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupCommuterPlan
        fields = ('company_group', )
