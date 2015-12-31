from app.models.health_benefits.company_group_benefit_plan_option import \
    CompanyGroupBenefitPlanOption
from app.serializers.company_group_serializer import \
    CompanyGroupSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase


class CompanyGroupBenefitPlanOptionGroupOnlySerializer(HashPkSerializerBase):
    company_group = CompanyGroupSerializer()

    class Meta:
        model = CompanyGroupBenefitPlanOption
        fields = ('company_group', )
