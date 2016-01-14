from app.models.insurance.company_group_std_insurance_plan import \
    CompanyGroupStdInsurancePlan
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupStdInsurancePlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupStdInsurancePlan
        fields = ('company_group', )
