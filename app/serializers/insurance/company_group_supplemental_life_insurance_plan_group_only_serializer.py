from app.models.insurance.company_group_suppl_life_insurance_plan import \
    CompanyGroupSupplLifeInsurancePlan
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupSupplementalLifeInsurancePlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupSupplLifeInsurancePlan
        fields = ('company_group', )
