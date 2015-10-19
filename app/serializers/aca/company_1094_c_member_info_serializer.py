from rest_framework import serializers
from app.models.aca.company_1094_c_member_info import Company1094CMemberInfo
from app.serializers.company_serializer import ShallowCompanySerializer
from ..hash_pk_serializer_base import HashPkSerializerBase

class Company1094CMemberInfoSerializer(HashPkSerializerBase):
    company = ShallowCompanySerializer()
    class Meta:
        model = Company1094CMemberInfo

class Company1094CMemberInfoPostSerializer(HashPkSerializerBase):
    class Meta:
        model = Company1094CMemberInfo
