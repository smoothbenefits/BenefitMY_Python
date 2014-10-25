from rest_framework import serializers

from company_serializer import CompanySerializer
from app.models.company_user import CompanyUser


class UserCompanyRolesSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = CompanyUser
        fields = ('id',
                  'company_user_type',
                  'company')
