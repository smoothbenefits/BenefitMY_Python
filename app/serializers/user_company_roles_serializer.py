from rest_framework import serializers

from app.models.company_user import CompanyUser


class UserCompanyRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyUser
        fields = ('id',
                  'company_user_type',
                  'company')
        depth = 1
