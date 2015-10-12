from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.extra_benefits.person_company_extra_benefit_plan import \
    PersonCompanyExtraBenefitPlan
from app.serializers.extra_benefits.company_extra_benefit_plan_serializer import (
    CompanyExtraBenefitPlanSerializer)
from app.serializers.extra_benefits.person_company_extra_benefit_plan_item_serializer \
    import (
        PersonCompanyExtraBenefitPlanItemSerializer,
        PersonCompanyExtraBenefitPlanItemPostSerializer)
from ..sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer


class PersonCompanyExtraBenefitPlanSerializer(HashPkSerializerBase):
    company_plan = CompanyExtraBenefitPlanSerializer()
    plan_items = PersonCompanyExtraBenefitPlanItemSerializer(many=True)
    person = HashField(source="person.id")
    record_reason = SysBenefitUpdateReasonSerializer()

    class Meta:
        model = PersonCompanyExtraBenefitPlan


class PersonCompanyExtraBenefitPlanPostSerializer(serializers.ModelSerializer):
    plan_items = PersonCompanyExtraBenefitPlanItemPostSerializer(
        many=True,
        required=False,
        allow_add_remove=True
    )

    class Meta:
        model = PersonCompanyExtraBenefitPlan
