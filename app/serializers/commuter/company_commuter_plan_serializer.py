from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.commuter.company_commuter_plan import CompanyCommuterPlan


class CompanyCommuterPlanSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyCommuterPlan

class CompanyCommuterPlanPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyCommuterPlan
