from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.hra.person_company_hra_plan import \
    PersonCompanyHraPlan
from company_hra_plan_serializer import (
    CompanyHraPlanSerializer,
    CompanyHraPlanPostSerializer)
from ..sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer

class PersonCompanyHraPlanSerializer(HashPkSerializerBase):
    company_hra_plan = CompanyHraPlanSerializer()
    person = HashField(source="person.id")
    record_reason = SysBenefitUpdateReasonSerializer()

    class Meta:
        model = PersonCompanyHraPlan

class PersonCompanyHraPlanPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonCompanyHraPlan
