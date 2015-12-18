from rest_framework import serializers
from app.models.hsa.person_company_group_hsa_plan import PersonCompanyGroupHsaPlan
from company_group_hsa_plan_serializer import CompanyGroupHsaPlanSerializer
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField
from ..sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer

class PersonCompanyGroupHsaPlanSerializer(HashPkSerializerBase):

    person = HashField(source="person.id")
    company_group_hsa_plan = CompanyGroupHsaPlanSerializer()
    record_reason = SysBenefitUpdateReasonSerializer()

    class Meta:
        model = PersonCompanyGroupHsaPlan

class PersonCompanyGroupHsaPlanPostSerializer(HashPkSerializerBase):

    class Meta:
        model = PersonCompanyGroupHsaPlan
