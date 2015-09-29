from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.commuter.person_company_commuter_plan import \
    PersonCompanyCommuterPlan
from company_commuter_plan_serializer import (
    CompanyCommuterPlanSerializer,
    CompanyCommuterPlanPostSerializer)


class PersonCompanyCommuterPlanSerializer(HashPkSerializerBase):
    company_commuter_plan = CompanyCommuterPlanSerializer()
    person = HashField(source="person.id")

    class Meta:
        model = PersonCompanyCommuterPlan

class PersonCompanyCommuterPlanPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonCompanyCommuterPlan
