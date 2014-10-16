from rest_framework import serializers

from user_serializer import UserSerializer
from app.models.company_user import CompanyUser


class CompanyUserSerializer(serializers.ModelSerializer):
    users = UserSerializer(source='user_set', many=True)
    class Meta:
        model = CompanyUser
