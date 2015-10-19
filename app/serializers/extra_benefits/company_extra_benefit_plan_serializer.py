from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.extra_benefits.company_extra_benefit_plan \
    import CompanyExtraBenefitPlan
from app.serializers.extra_benefits.extra_benefit_item_serializer \
    import ExtraBenefitItemSerializer, ExtraBenefitItemPostSerializer


class CompanyExtraBenefitPlanSerializer(HashPkSerializerBase):
    benefit_items = ExtraBenefitItemSerializer(many=True)
    company = HashField(source="company.id")

    class Meta:
        model = CompanyExtraBenefitPlan


class CompanyExtraBenefitPlanPostSerializer(serializers.ModelSerializer):
    benefit_items = ExtraBenefitItemPostSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = CompanyExtraBenefitPlan
