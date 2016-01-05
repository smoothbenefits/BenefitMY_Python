from app.models.insurance.company_group_ltd_insurance_plan import \
    CompanyGroupLtdInsurancePlan
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupLtdInsurancePlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupLtdInsurancePlan
        fields = ('company_group', )
