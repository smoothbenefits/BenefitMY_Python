from rest_framework import serializers
from app.models.company_user import CompanyUser
from company_serializer import ShallowCompanySerializer
from hash_pk_serializer_base import HashPkSerializerBase


class UserCompanyRolesSerializer(HashPkSerializerBase):

	company = ShallowCompanySerializer()

	class Meta:
		model = CompanyUser
		fields = ('id',
			'company_user_type',
			'company', 
			'new_employee')
