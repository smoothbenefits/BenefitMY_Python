from app.models.insurance.company_group_basic_life_insurance_plan import \
    CompanyGroupBasicLifeInsurancePlan
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupBasicLifeInsurancePlanGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupBasicLifeInsurancePlan
        fields = ('company_group', )
