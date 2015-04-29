from rest_framework import serializers
from app.models.fsa.user_company_fsa_plan import UserCompanyFsaPlan
from company_fsa_plan_serializer import (
    CompanyFsaPlanSerializer,
    CompanyFsaPlanPostSerializer)
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class UserCompanyFsaPlanSerializer(HashPkSerializerBase):
    user = HashField(source="user.id")
    company_fsa_plan = CompanyFsaPlanSerializer()

    class Meta:
        model = UserCompanyFsaPlan


class UserCompanyFsaPlanPostSerializer(serializers.ModelSerializer):
    company_fsa_plan = CompanyFsaPlanPostSerializer()

    class Meta:
        model = UserCompanyFsaPlan
