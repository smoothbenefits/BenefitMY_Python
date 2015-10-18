from rest_framework import serializers
from app.models.aca.company_1094_c_monthly_member_info import Company1094CMonthlyMemberInfo
from app.serializers.company_serializer import ShallowCompanySerializer
from ..hash_pk_serializer_base import HashPkSerializerBase

class Company1094CMonthlyMemberInfoSerializer(HashPkSerializerBase):
    company = ShallowCompanySerializer()
    class Meta:
        model = Company1094CMonthlyMemberInfo

class Company1094CMonthlyMemberInfoPostSerializer(HashPkSerializerBase):
    class Meta:
        model = Company1094CMonthlyMemberInfo
