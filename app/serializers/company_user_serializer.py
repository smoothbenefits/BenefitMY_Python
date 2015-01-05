from rest_framework import serializers

from user_serializer import UserSerializer
from app.models.company_user import CompanyUser


class CompanyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyUser
        fields = ('id',
                  'company_user_type',
                  'user',
                  'new_employee')

        depth = 1

class CompanyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyUser
        fields = ('id',
                  'company_user_type',
                  'new_employee')
