from rest_framework import serializers

from user_serializer import UserSerializer
from app.models.company_user import CompanyUser


class CompanyUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CompanyUser
        fields = ('id',
                  'company_user_type',
                  'user')
