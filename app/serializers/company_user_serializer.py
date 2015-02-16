from rest_framework import serializers

from user_serializer import UserSerializer
from app.models.company_user import CompanyUser
from hash_pk_serializer_base import HashPkSerializerBase


class CompanyUserSerializer(HashPkSerializerBase):

    user = UserSerializer()
    class Meta:
        model = CompanyUser
        fields = ('id',
                  'company_user_type',
                  'user',
                  'new_employee')

class CompanyRoleSerializer(HashPkSerializerBase):
    class Meta:
        model=CompanyUser
        fields = ('id',
                  'company_user_type',
                  'new_employee')
