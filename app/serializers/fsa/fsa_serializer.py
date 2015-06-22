from rest_framework import serializers
from app.models.fsa.fsa import FSA
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField
from ..sys_benefit_update_reason_serializer import SysBenefitUpdateReasonSerializer

class FsaSerializer(HashPkSerializerBase):

    user = HashField(source="user.id")
    company_fsa_plan = HashField(source="company_fsa_plan.id")
    record_reason = SysBenefitUpdateReasonSerializer()

    class Meta:
        model = FSA

class FsaPostSerializer(HashPkSerializerBase):
    
    class Meta:
        model = FSA
