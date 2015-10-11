from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.extra_benefits.person_company_extra_benefit_plan_item \
    import PersonCompanyExtraBenefitPlanItem
from app.serializers.extra_benefits.extra_benefit_item_serializer \
    import ExtraBenefitItemSerializer


class PersonCompanyExtraBenefitPlanItemSerializer(HashPkSerializerBase):
    person_company_extra_benefit_plan = HashField(source="person_company_extra_benefit_plan.id")
    extra_benefit_item = ExtraBenefitItemSerializer()

    class Meta:
        model = PersonCompanyExtraBenefitPlanItem


class PersonCompanyExtraBenefitPlanItemPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonCompanyExtraBenefitPlanItem
